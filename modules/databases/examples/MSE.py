import json
import os
import sys
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)


from mse.core import MorphicSemanticEngine
from modules.databases.Statistics import Statistics


class MSE:

    def __init__(self, output_dir: str = None, mod: int = 9973, **kwargs) -> None:
        super(MSE, self).__init__(**kwargs)
        self.mod = mod
        if output_dir is None:
            # e.g. src/modules/databases/mse_output
            self.output_dir = os.path.join(PROJECT_ROOT, "databases", "output", "mse_output")
        else:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -------------------------------
    # Core helpers (same logic as Streamlit app)
    # -------------------------------
    def build_engine_and_seed_from_days(
        self,
        days: List[Dict[str, Any]],
        stats: Statistics,
    ):
        """
        Given a list of per-day stats dicts:
        - Aggregate into a profile
        - Build base signature
        - Encode full 30-day series to series_seed
        - Augment signature with series_seed
        - Initialize MorphicSemanticEngine
        """
        profile = stats.aggregate_profile_from_30days(days)
        base_signature = stats.profile_to_signature(profile)
        series_seed = stats.encode_30day_stats(days)
        augmented_signature = stats.augment_signature_with_series(base_signature, series_seed)

        vocab = [str(i) for i in range(27)]
        constants = {"a": 3, "b": 5, "c": 7, "d": 11}

        engine = MorphicSemanticEngine(
            initial_state=tuple(augmented_signature),
            vocab=vocab,
            constants=constants,
            mod=self.mod,
        )

        mse_storage = {
            "user_id": profile["user_id"],
            "signature": list(base_signature),
            "series_seed": series_seed,
            "mod": self.mod,
            "constants": constants,
        }

        return engine, profile, base_signature, series_seed, augmented_signature, mse_storage

    # -------------------------------
    # Main export entrypoint
    # -------------------------------
    def main(self):
        """
        Default: build 30-day synthetic stats using Statistics,
        derive the MSE minimal stored object, and export to JSON.
        """
        stats = Statistics()
        days = stats.get_30day_stats()

        (
            engine,
            profile,
            base_signature,
            series_seed,
            augmented_signature,
            mse_storage,
        ) = self.build_engine_and_seed_from_days(days, stats)

        # Export minimal stored object
        user_id = profile.get("user_id", "user_mse")
        filename = f"{user_id}_mse_minimal_seed.json"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "mse_storage": mse_storage,
                    "profile": profile,
                    "base_signature": base_signature,
                    "augmented_signature": augmented_signature,
                    "series_seed": series_seed,
                },
                f,
                indent=4,
            )

        print(f"[MSEExporter] Wrote minimal MSE export to: {path}")


if __name__ == "__main__":
    MSE().main()

import json
import os
import sys
from typing import Dict, Any, List

# Find project root (two levels up from this file: modules/examples/.. /..)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

"""
firebase_tables.py

Generate Firebase/Firestore-style JSON documents from MSE engine steps, using:
- 30-day stats compressed into a minimal seed via Statistics
- MorphicSemanticEngine
- TableData.capture_state(engine)
"""

from mse.core import MorphicSemanticEngine
from modules.databases.TableData import TableData
from modules.databases.Statistics import Statistics


class Firebase:

    def __init__(self, **kwargs):
        super(Firebase, self).__init__(**kwargs)

    def main(self):
        output_dir = os.path.join(PROJECT_ROOT, "databases", "output", "firebase_output")
        os.makedirs(output_dir, exist_ok=True)

        stats = Statistics()

        # 1) Get 30-day stats
        days = stats.get_30day_stats()

        # 2) Aggregate and get base signature
        profile = stats.aggregate_profile_from_30days(days)
        base_signature = stats.profile_to_signature(profile)

        # 3) Encode series + augment signature
        series_seed = stats.encode_30day_stats(days)
        augmented_signature = stats.augment_signature_with_series(base_signature, series_seed)

        print("User ID:", profile["user_id"])
        print("Base signature:", base_signature)
        print("Series seed:", series_seed)
        print("Augmented signature:", augmented_signature)

        # 4) Initialize MSE
        vocab = [str(i) for i in range(27)]
        constants = {"a": 3, "b": 5, "c": 7, "d": 11}

        engine = MorphicSemanticEngine(
            initial_state=tuple(augmented_signature),
            vocab=vocab,
            constants=constants,
            mod=9973,
        )

        db = TableData()
        steps = 30  # treat t = 1..30 as days

        for _ in range(steps):
            engine.step()
            schema = db.capture_state(engine)
            t = engine.t

            # Firestore-style document structure
            doc = {
                "user_id": profile["user_id"],
                "day_index": t,
                "table": schema["table"],
                "columns": [
                    {"name": name, "type": dtype}
                    for name, dtype in schema["columns"]
                ],
                "rows": schema["rows"],
                "mse_storage": {
                    "signature": list(base_signature),
                    "series_seed": series_seed,
                    "mod": 9973,
                    "constants": {"a": 3, "b": 5, "c": 7, "d": 11},
                },
            }

            filename = os.path.join(output_dir, f"firebase_day_{t:03}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(doc, f, indent=4)

            print(f"Generated {filename} for user", profile["user_id"])


if __name__ == "__main__":
    Firebase().main()

import json
import os
import sys
from typing import Dict, Any

# Find project root (two levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

"""
DynamoDB export example with full user profile

Flow:
- Load/build a full user profile.
- Map profile -> MSE signature (minimal stored state).
- Initialize MorphicSemanticEngine from signature.
- Use TableData to turn engine state into table schema/rows.
- Export each step as a DynamoDB-style JSON item.
"""

from modules.databases.Statistics import Statistics
from mse.core import MorphicSemanticEngine
from modules.databases.TableData import TableData


def to_ddb_str(value: str) -> dict:
    return {"S": value}


# -------------------------------
# User profile + signature mapping
# -------------------------------

def get_example_user_profile() -> Dict[str, Any]:
    """Simulate a full profile from your main app database."""
    return {
        "user_id": "u_12345",
        "email": "alex@example.com",
        "name": "Alex Carter",
        "age": 31,
        "location": "Sacramento, CA",
        "fitness_level": "intermediate",  # beginner / intermediate / advanced
        "stress_level": "high",           # low / medium / high
        "sleep_quality": "poor",          # poor / ok / good
        "work_type": "desk_job",
        "interests": ["running", "sci-fi", "city_builders"],
        "created_at": "2025-11-01T12:34:56Z",
    }


def profile_to_signature(profile: Dict[str, Any]) -> tuple[int, int, int, int, int]:
    """
    Map rich profile data → (health, cognition, stress, strength, lifestyle).
    This is your minimal MSE seed per user.
    """
    fitness_map = {"beginner": 40, "intermediate": 65, "advanced": 85}
    stress_map = {"low": 25, "medium": 50, "high": 75}
    sleep_map = {"poor": 35, "ok": 60, "good": 80}

    h = fitness_map.get(profile.get("fitness_level", "beginner"), 50)
    c = 60
    st = stress_map.get(profile.get("stress_level", "medium"), 50)
    strn = min(100, h + 5)
    life = sleep_map.get(profile.get("sleep_quality", "ok"), 60)

    return (h, c, st, strn, life)




class DynamoDB:

    def __init__(self, **kwargs):
        super(DynamoDB, self).__init__(**kwargs)

        self.session = Statistics()

    def main(self):
        # Output directory under project root
        output_dir = os.path.join(PROJECT_ROOT, "databases", "output", "dynamodb_output")
        os.makedirs(output_dir, exist_ok=True)

        # 1) Get 30-day per-day stats
        days = self.session.get_30day_stats()

        # 2) Aggregate into a profile
        profile = self.session.aggregate_profile_from_30days(days)

        # 3) Build base MSE signature from aggregate profile
        base_signature = profile_to_signature(profile)

        # 4) Encode full 30-day series into ONE integer
        series_seed = self.session.encode_30day_stats(days)

        # 5) Augment signature with series_seed (still only 5 ints!)
        augmented_signature = self.session.augment_signature_with_series(base_signature, series_seed)

        print("User ID:", profile["user_id"])
        print("Base signature:", base_signature)
        print("Series seed:", series_seed)
        print("Augmented signature:", augmented_signature)

        # 6) MSE engine config
        vocab = [str(i) for i in range(27)]
        constants = {"a": 3, "b": 5, "c": 7, "d": 11}

        engine = MorphicSemanticEngine(
            initial_state=tuple(augmented_signature),
            vocab=vocab,
            constants=constants,
            mod=9973,
        )

        db = TableData()

        # Interpret t = 1..30 as "day index" driven by the same seed
        steps = 30

        for _ in range(steps):
            engine.step()
            schema = db.capture_state(engine)
            t = engine.t  # treating as "day t"

            item = {
                "t": {"N": str(t)},
                "user_id": {"S": profile["user_id"]},
                "table": {"S": schema["table"]},
                "columns": {
                    "L": [
                        {
                            "M": {
                                "name": to_ddb_str(col_name),
                                "dtype": to_ddb_str(dtype),
                            }
                        }
                        for col_name, dtype in schema["columns"]
                    ]
                },
                "rows": {
                    "L": [
                        {"L": [to_ddb_str(v) for v in row]}
                        for row in schema["rows"]
                    ]
                },
                # Minimal seed storage meta (what you'd actually persist)
                "mse_storage": {
                    "M": {
                        "signature": {
                            "L": [{"N": str(x)} for x in base_signature]
                        },
                        "series_seed": {"N": str(series_seed)},
                        "mod": {"N": "9973"},
                    }
                },
            }

            filename = os.path.join(output_dir, f"dynamodb_t{t:03}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(item, f, indent=4)

            print(f"Generated {filename} for user", profile["user_id"])


if __name__ == "__main__":
    DynamoDB().main()

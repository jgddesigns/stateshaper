import os
import sys
from typing import Dict, Any, List

# Find project root (two levels up from this file: modules/examples/.. /..)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

"""
sql_tables.py

Generate MySQL-like .sql files from MSE engine steps, using:
- 30-day stats compressed into a minimal seed via Statistics
- MorphicSemanticEngine
- TableData.capture_state(engine)
"""

from mse.core import MorphicSemanticEngine
from modules.databases.TableData import TableData
from modules.databases.Statistics import Statistics


class MySQL:

    def __init__(self, **kwargs):
        super(MySQL, self).__init__(**kwargs)

    @staticmethod
    def create_sql(table: str, columns: List[tuple]) -> str:
        lines = [f"CREATE TABLE `{table}` ("]
        col_lines = [f"  `{name}` {dtype}" for name, dtype in columns]
        lines.append(",\n".join(col_lines))
        lines.append(");")
        return "\n".join(lines)

    @staticmethod
    def insert_sql(table: str, columns: List[tuple], rows: List[List[str]]) -> str:
        col_names = ", ".join(f"`{name}`" for name, _ in columns)
        inserts = []
        for row in rows:
            values = ", ".join(f"'{v}'" for v in row[:len(columns)])
            inserts.append(f"INSERT INTO `{table}` ({col_names}) VALUES ({values});")
        return "\n".join(inserts)

    def main(self):
        output_dir = os.path.join(PROJECT_ROOT, "databases", "output", "sql_output")
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

            table = schema["table"]
            columns = schema["columns"]
            rows = schema["rows"]

            create_stmt = self.create_sql(table, columns)
            insert_stmts = self.insert_sql(table, columns, rows)

            # Add minimal mse_storage metadata as a SQL comment header
            header = (
                f"-- mse_storage.user_id={profile['user_id']}\n"
                f"-- mse_storage.signature={base_signature}\n"
                f"-- mse_storage.series_seed={series_seed}\n"
                f"-- mse_storage.mod=9973\n\n"
            )

            filename = os.path.join(output_dir, f"stats_day_{t:03}.sql")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(header)
                f.write(create_stmt)
                f.write("\n\n")
                f.write(insert_stmts)
                f.write("\n")

            print(f"Generated {filename} for user", profile["user_id"])


if __name__ == "__main__":
    MySQL().main()

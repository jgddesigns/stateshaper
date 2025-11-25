import os
import sys

# Find project root (two levels up from this file: modules/personalization/.. /..)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

"""
database_plugin.py

A sidecar plugin that attaches to MorphicSemanticEngine and
generates MySQL database schema/data *at each engine step*.

This file does NOT modify the engine.
It only reads:

    engine.state    (list[int])
    engine.t        (int)

and outputs:

    - table name
    - columns
    - row data
    - CREATE TABLE SQL
    - INSERT SQL

Everything is deterministic based on the MSE numeric state.
"""

from typing import List, Dict, Any


# =============================================================
# 1. Vocabulary Tables (swap freely)
# =============================================================

TABLE_NAMES = [
    "users", "orders", "products", "logs", "sessions",
    "events", "messages", "profiles", "inventory", "metrics"
]

COLUMN_NAMES = [
    "id", "uuid", "name", "email", "timestamp",
    "value", "amount", "status", "type", "category"
]

DATA_TYPES = [
    "INT", "VARCHAR(255)", "TEXT", "DATETIME",
    "FLOAT", "BOOLEAN"
]

DATA_VALUES = [
    "alpha", "bravo", "charlie", "delta", "echo",
    "foxtrot", "golf", "hotel", "india", "juliet"
]


# =============================================================
# 2. The Plugin Class
# =============================================================

class TableData:
    """
    A plugin that listens to MSE engine steps.

    Usage:
        engine = MorphicSemanticEngine(...)
        db = TableData()

        token = engine.step()
        schema = db.capture_state(engine)   # schema for this step

    Or automatically on each step by wrapping engine.step().
    """

    def __init__(
        self,
        table_vocab: List[str] = TABLE_NAMES,
        column_vocab: List[str] = COLUMN_NAMES,
        datatype_vocab: List[str] = DATA_TYPES,
        data_vocab: List[str] = DATA_VALUES,
    ):
        self.table_vocab = table_vocab
        self.column_vocab = column_vocab
        self.datatype_vocab = datatype_vocab
        self.data_vocab = data_vocab

    # ---------------------------------------------------------
    # Convert state → table schema
    # ---------------------------------------------------------
    def state_to_table(self, state: List[int]) -> Dict[str, Any]:
        table_name = self.table_vocab[state[0] % len(self.table_vocab)]
        col_count = (state[1] % 5) + 2  # 2–6 columns

        columns = []
        n = len(state)
        for i in range(col_count):
            col_name = self.column_vocab[state[(2 + i) % n] % len(self.column_vocab)]
            col_type = self.datatype_vocab[state[(2 + col_count + i) % n] % len(self.datatype_vocab)]
            columns.append((col_name, col_type))

        return {"table": table_name, "columns": columns}

    # ---------------------------------------------------------
    # Convert state → row data
    # ---------------------------------------------------------
    def state_to_rows(self, state: List[int], max_rows: int = 5) -> List[List[str]]:
        row_count = (state[0] % max_rows) + 1
        vocab_size = len(self.data_vocab)

        rows = []
        for _ in range(row_count):
            row = [self.data_vocab[v % vocab_size] for v in state]
            rows.append(row)
        return rows

    # ---------------------------------------------------------
    # SQL Builders
    # ---------------------------------------------------------
    def create_sql(self, table: str, columns: List[tuple]) -> str:
        body = ",\n".join(f"  `{name}` {dtype}" for name, dtype in columns)
        return f"CREATE TABLE `{table}` (\n{body}\n);"

    def insert_sql(self, table: str, columns: List[tuple], rows: List[List[str]]) -> str:
        col_names = ", ".join(f"`{n}`" for n, _ in columns)
        stmts = []

        for row in rows:
            vals = [f"'{v}'" for v in row[:len(columns)]]
            stmts.append(f"INSERT INTO `{table}` ({col_names}) VALUES ({', '.join(vals)});")

        return "\n".join(stmts)

    # ---------------------------------------------------------
    # MAIN PLUGIN ENTRY POINT
    # ---------------------------------------------------------
    def capture_state(self, engine: Any) -> Dict[str, Any]:
        """
        Capture the database representation for the CURRENT state of the engine.

        Does not advance the engine.
        Does not modify the engine.
        """

        state = engine.state      # live engine state
        t = engine.t              # current time index

        table_info = self.state_to_table(state)
        table = table_info["table"]
        columns = table_info["columns"]
        rows = self.state_to_rows(state)

        return {
            "t": t,
            "table": table,
            "columns": columns,
            "rows": rows,
            "create_sql": self.create_sql(table, columns),
            "insert_sql": self.insert_sql(table, columns, rows),
        }

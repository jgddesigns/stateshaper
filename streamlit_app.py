import os
import sys
import json
from io import BytesIO
from typing import Dict, Any, List

import streamlit as st
import pandas as pd

# -------------------------------
# Project path setup
# -------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

# -------------------------------
# Internal imports
# -------------------------------
from mse.core import MorphicSemanticEngine
from modules.databases.TableData import TableData
from modules.databases.Statistics import Statistics

# Optional: backend exporter classes (full 30-day file export)
try:
    from modules.databases.examples.MySQL import MySQL as SQLExporter
except ImportError:
    SQLExporter = None

try:
    from modules.databases.examples.MongoDB import MongoDB as MongoExporter
except ImportError:
    MongoExporter = None

try:
    from modules.databases.examples.Firebase import Firebase as FirebaseExporter
except ImportError:
    FirebaseExporter = None

try:
    from modules.databases.examples.DynamoDB import DynamoDB as DynamoExporter
except ImportError:
    DynamoExporter = None

try:
    from modules.databases.examples.MSE import MSE as MSEExporter
except ImportError:
    MSEExporter = None



# -------------------------------
# DB format helper functions
# -------------------------------

def format_sql(schema: Dict[str, Any], profile: Dict[str, Any], base_signature, series_seed) -> str:
    table = schema["table"]
    columns = schema["columns"]
    rows = schema["rows"]

    lines = []
    # Header with minimal seed info
    lines.append(f"-- user_id={profile['user_id']}")
    lines.append(f"-- signature={base_signature}")
    lines.append(f"-- series_seed={series_seed}")
    lines.append(f"-- mod=9973")
    lines.append("")

    # CREATE TABLE
    lines.append(f"CREATE TABLE `{table}` (")
    col_lines = [f"  `{name}` {dtype}" for name, dtype in columns]
    lines.append(",\n".join(col_lines))
    lines.append(");")
    lines.append("")

    # INSERTs
    col_names = ", ".join(f"`{name}`" for name, _ in columns)
    for row in rows:
        values = ", ".join(f"'{v}'" for v in row[:len(columns)])
        lines.append(f"INSERT INTO `{table}` ({col_names}) VALUES ({values});")

    return "\n".join(lines)


def format_mongo(schema: Dict[str, Any], profile: Dict[str, Any], base_signature, series_seed, t: int) -> str:
    doc = {
        "_id": f"{profile['user_id']}_day_{t}",
        "user_id": profile["user_id"],
        "day_index": t,
        "table": schema["table"],
        "columns": [
            {"name": col_name, "type": dtype}
            for col_name, dtype in schema["columns"]
        ],
        "rows": schema["rows"],
        "mse_storage": {
            "signature": list(base_signature),
            "series_seed": series_seed,
            "mod": 9973,
            "constants": {"a": 3, "b": 5, "c": 7, "d": 11},
        },
    }
    return json.dumps(doc, indent=4)


def format_firebase(schema: Dict[str, Any], profile: Dict[str, Any], base_signature, series_seed, t: int) -> str:
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
    return json.dumps(doc, indent=4)


def to_ddb_str(value: str) -> Dict[str, str]:
    return {"S": value}


def format_dynamo(schema: Dict[str, Any], profile: Dict[str, Any], base_signature, series_seed, t: int) -> str:
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
        "mse_storage": {
            "M": {
                "signature": {"L": [{"N": str(x)} for x in base_signature]},
                "series_seed": {"N": str(series_seed)},
                "mod": {"N": "9973"},
            }
        },
    }
    return json.dumps(item, indent=4)


# -------------------------------
# Engine + seed helpers
# -------------------------------

def build_engine_and_seed_from_days(days: List[Dict[str, Any]], stats: Statistics):
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
        mod=9973,
    )

    mse_storage = {
        "user_id": profile["user_id"],
        "signature": list(base_signature),
        "series_seed": series_seed,
        "mod": 9973,
        "constants": constants,
    }

    return engine, profile, base_signature, series_seed, augmented_signature, mse_storage


def run_engine_with_tabledata(engine: MorphicSemanticEngine, steps: int = 30):
    """Run the engine for `steps` and capture TableData schemas per t."""
    db = TableData()
    schemas_by_t: Dict[int, Dict[str, Any]] = {}
    for _ in range(steps):
        engine.step()
        schemas_by_t[engine.t] = db.capture_state(engine)
    return schemas_by_t


def build_stats_schema(days: List[Dict[str, Any]], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a DB-friendly schema from the 30-day stats:
    day, treadmill_minutes, avg_daily_steps, calories, protein_g, sleep_hours
    """
    table_name = f"{profile.get('user_id', 'user')}_30day_stats"

    columns = [
        ("day", "INT"),
        ("treadmill_minutes", "INT"),
        ("avg_daily_steps", "INT"),
        ("calories", "INT"),
        ("protein_g", "INT"),
        ("sleep_hours", "FLOAT"),
    ]

    rows = []
    for d in days:
        rows.append([
            int(d["day_index"] + 1),                     # 1–30, internal day_index is still 0–29
            int(d["treadmill_minutes"]),
            int(d["avg_daily_steps"]),
            int(d["calories"]),
            int(d["protein_g"]),
            float(d["sleep_hours"]),
        ])

    return {
        "table": table_name,
        "columns": columns,
        "rows": rows,
    }




# -------------------------------
# Streamlit app
# -------------------------------

def main():
    st.set_page_config(page_title="MSE DB Formats Demo", layout="wide")

    st.title("Morphic Semantic Engine – DB Format Demo")
    st.caption("Edit 30-day stats → build minimal seed → view & export SQL / Mongo / Firebase / DynamoDB.")

    stats = Statistics()

    # ---------------------------------------------------------
    # Section 1: Editable 30-day stats
    # ---------------------------------------------------------
    st.subheader("1. Edit 30-Day Statistics")

    default_days = stats.get_30day_stats()
    df_default = pd.DataFrame(default_days)[
        ["day_index", "treadmill_minutes", "avg_daily_steps", "calories", "protein_g", "sleep_hours"]
    ]
    df_default["day"] = df_default["day_index"] + 1
    df_default = df_default[
        ["day", "day_index", "treadmill_minutes", "avg_daily_steps", "calories", "protein_g", "sleep_hours"]
    ]

    st.markdown(
        "Use the table below to adjust treadmill minutes, steps, calories, protein, and sleep "
        "for each day. These stats feed into the MSE seed used for all DB formats."
    )

    edited_df = st.data_editor(
        df_default,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "day": st.column_config.NumberColumn("Day", disabled=True),
            "day_index": st.column_config.NumberColumn("day_index", disabled=True),
        },
        key="stats_editor",
    )

    # Convert edited DataFrame back into days list
    days: List[Dict[str, Any]] = []
    for _, row in edited_df.iterrows():
        days.append(
            {
                "day_index": int(row["day_index"]),
                "treadmill_minutes": float(row["treadmill_minutes"]),
                "avg_daily_steps": float(row["avg_daily_steps"]),
                "calories": float(row["calories"]),
                "protein_g": float(row["protein_g"]),
                "sleep_hours": float(row["sleep_hours"]),
            }
        )

    # Quick charts
    col_chart1, col_chart2 = st.columns(2)
    df_days_display = pd.DataFrame(days)
    df_days_display["day"] = df_days_display["day_index"] + 1
    df_days_display = df_days_display[
        ["day", "treadmill_minutes", "avg_daily_steps", "calories", "protein_g", "sleep_hours"]
    ]

    with col_chart1:
        st.markdown("**Treadmill Minutes & Sleep**")
        st.line_chart(df_days_display.set_index("day")[["treadmill_minutes", "sleep_hours"]])

    with col_chart2:
        st.markdown("**Steps & Calories**")
        st.line_chart(df_days_display.set_index("day")[["avg_daily_steps", "calories"]])

    # ---------------------------------------------------------
    # Section 2: Seed from edited stats
    # ---------------------------------------------------------
    st.subheader("2. Minimal Seed Derived from Your Stats")

    engine, profile, base_signature, series_seed, augmented_signature, mse_storage = build_engine_and_seed_from_days(
        days, stats
    )

    col_sig, col_seed = st.columns(2)

    with col_sig:
        st.markdown("**Aggregate Profile (from edited stats)**")
        st.json(profile)

        st.markdown("**Base Signature (5 ints)**")
        st.json(
            {
                "health": base_signature[0],
                "cognition": base_signature[1],
                "stress": base_signature[2],
                "strength": base_signature[3],
                "lifestyle": base_signature[4],
            }
        )

    with col_seed:
        st.markdown("**series_seed (single integer summarizing 30 days)**")
        st.write(series_seed)

        st.markdown("**Augmented Signature (used as initial_state)**")
        st.write(augmented_signature)

        st.markdown("**Minimal stored object (`mse_storage`)**")
        st.json(mse_storage)

    # ---------------------------------------------------------
    # Section 2.5: Live File Size Comparison
    # ---------------------------------------------------------
    # Run engine once here so we can use schemas for size estimation
    schemas_by_t = run_engine_with_tabledata(engine, steps=30)

    # Size of minimal seed (JSON)
    seed_json = json.dumps(mse_storage, separators=(",", ":"))
    seed_bytes = len(seed_json.encode("utf-8"))
    seed_kb = seed_bytes / 1024.0

    # Size of a "standard" full database:
    # - raw 30-day stats
    # - plus 30 Mongo-style docs (one per day)
    days_json = json.dumps(days, separators=(",", ":"))
    days_bytes = len(days_json.encode("utf-8"))

    mongo_total_bytes = 0
    for t, schema_t in schemas_by_t.items():
        mongo_doc = format_mongo(schema_t, profile, base_signature, series_seed, t)
        mongo_total_bytes += len(mongo_doc.encode("utf-8"))

    full_bytes = days_bytes + mongo_total_bytes
    full_kb = full_bytes / 1024.0

    ratio = full_kb / seed_kb if seed_kb > 0 else 0.0

    # Nice centered highlight
    st.markdown("### 2.5 Live Storage Footprint Comparison")
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin-top:10px; margin-bottom:25px;">
          <div style="background:linear-gradient(135deg,#111827,#1f2937); 
                      border-radius:18px; padding:28px 32px; 
                      text-align:center; max-width:700px; 
                      box-shadow:0 12px 30px rgba(0,0,0,0.45);">
            <div style="font-size:25px; font-weight:600; color:#e5e7eb; letter-spacing:0.04em; text-transform:uppercase;">
              Storage Comparison (Live)
            </div>
            <div style="margin-top:14px; font-size:35px; font-weight:700; color:#fbbf24;">
              MSE Seed: {seed_kb:.2f} KB &nbsp;&nbsp;vs&nbsp;&nbsp; Full DB: {full_kb:.2f} KB
            </div>
            <div style="margin-top:10px; font-size:18px; color:#9ca3af;">
              ≈ <span style="font-weight:600; color:#a5b4fc;">{ratio:,.0f}×</span> smaller using the MSE minimal seed
            </div>
            <div style="margin-top:8px; font-size:14px; color:#6b7280;">
              Updates automatically as you edit the 30-day stats above.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ---------------------------------------------------------
    # Section 2.6: Multi-user storage projection
    # ---------------------------------------------------------
    def format_size(bytes_val: float) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(bytes_val)
        unit_idx = 0
        while size >= 1024 and unit_idx < len(units) - 1:
            size /= 1024.0
            unit_idx += 1
        return f"{size:.2f} {units[unit_idx]}"

    user_counts = [10_000, 100_000, 1_000_000]
    rows_html = ""

    for n in user_counts:
        seed_total = seed_bytes * n
        full_total = full_bytes * n
        ratio_n = (full_total / seed_total) if seed_total > 0 else 0.0

        rows_html += f"""
          <tr>
            <td style="padding:8px 12px; text-align:left; font-weight:600; color:#e5e7eb;">
              {n:,} users
            </td>
            <td style="padding:8px 12px; text-align:right; color:#bbf7d0;">
              {format_size(seed_total)}
            </td>
            <td style="padding:8px 12px; text-align:right; color:#fee2e2;">
              {format_size(full_total)}
            </td>
            <td style="padding:8px 12px; text-align:right; color:#a5b4fc;">
              {ratio_n:,.0f}×
            </td>
          </tr>
        """

    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin-top:5px; margin-bottom:30px;">
          <div style="background:linear-gradient(135deg,#020617,#111827); 
                      border-radius:18px; padding:20px 26px; 
                      text-align:center; max-width:800px; 
                      box-shadow:0 10px 25px rgba(0,0,0,0.5);">
            <div style="font-size:22px; font-weight:600; color:#e5e7eb; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:10px;">
              At Scale (Per Current Stats & Schema)
            </div>
            <table style="width:100%; border-collapse:collapse; font-size:20px;">
              <thead>
                <tr>
                  <th style="padding:8px 12px; text-align:left; color:#9ca3af; font-weight:600; border-bottom:1px solid #374151;">
                    Users
                  </th>
                  <th style="padding:8px 12px; text-align:right; color:#9ca3af; font-weight:600; border-bottom:1px solid #374151;">
                    Total MSE Storage
                  </th>
                  <th style="padding:8px 12px; text-align:right; color:#9ca3af; font-weight:600; border-bottom:1px solid #374151;">
                    Total Full DB Storage
                  </th>
                  <th style="padding:8px 12px; text-align:right; color:#9ca3af; font-weight:600; border-bottom:1px solid #374151;">
                    Savings
                  </th>
                </tr>
              </thead>
              <tbody>
                {rows_html}

        """,
        unsafe_allow_html=True,
    )


    # ---------------------------------------------------------
    # Section 3: Choose format + preview + EXPORT button
    # ---------------------------------------------------------
    st.subheader("3. View & Export Data")

    col_controls, _ = st.columns([1, 3])

    with col_controls:
        db_choice = st.selectbox(
            "Output Format",
            options=[
                "MSE (30-day stats table)",
                "MongoDB (30-day stats table)",
                "Firebase (30-day stats table)",
                "DynamoDB (30-day stats table)",
                "SQL (30-day stats table)",
            ],
            index=0,
        )

    # Build schema from the actual 30-day stats
    stats_schema = build_stats_schema(days, profile)

    # Determine content + filename based on selection
    if db_choice == "MSE (30-day stats table)":
        formatted_output = json.dumps(mse_storage, indent=4)
        filename = f"{profile['user_id']}_mse_minimal_seed.json"
        language = "json"
        preview_title = "**MSE Stored Object (`mse_storage`)**"

    else:
        # All four DB formats use the 30-day stats table
        if db_choice.startswith("SQL"):
            formatted_output = format_sql(stats_schema, profile, base_signature, series_seed)
            filename = f"{profile['user_id']}_30day_stats.sql"
            language = "sql"
            preview_title = "**SQL Representation (30-Day Statistics)**"

        elif db_choice.startswith("MongoDB"):
            formatted_output = format_mongo(stats_schema, profile, base_signature, series_seed, t=0)
            filename = f"{profile['user_id']}_30day_stats_mongo.json"
            language = "json"
            preview_title = "**MongoDB Document (30-Day Statistics)**"

        elif db_choice.startswith("Firebase"):
            formatted_output = format_firebase(stats_schema, profile, base_signature, series_seed, t=0)
            filename = f"{profile['user_id']}_30day_stats_firebase.json"
            language = "json"
            preview_title = "**Firebase / Firestore Document (30-Day Statistics)**"

        elif db_choice.startswith("DynamoDB"):
            formatted_output = format_dynamo(stats_schema, profile, base_signature, series_seed, t=0)
            filename = f"{profile['user_id']}_30day_stats_dynamo.json"
            language = "json"
            preview_title = "**DynamoDB Item (30-Day Statistics)**"

    # -------------------------
    # Preview + export button
    # -------------------------
    st.markdown(preview_title)
    st.code(formatted_output, language=language)

    st.download_button(
        label="📥 Export File",
        data=formatted_output.encode("utf-8"),
        file_name=filename,
        mime="application/json" if filename.endswith(".json") else "text/plain",
        use_container_width=True,
    )



    # ---------------------------------------------------------
    # Section 4: Call backend exporter classes (full 30-day export)
    # ---------------------------------------------------------
    st.subheader("4. Full 30-Day Export via Backend Classes")

    st.markdown(
        "Use the buttons below to run your backend exporter classes. "
        "They will generate full 30-day output files under `modules/databases/*_output`."
    )

    col_exp1, col_exp2, col_exp3, col_exp4, col_exp5 = st.columns(5)

    with col_exp1:
        if st.button("Run MSE Exporter (30 days)"):
            if MSEExporter is None:
                st.warning("MSEExporter class not found (modules.databases.examples.MSE.MSE).")
            else:
                MSEExporter().main()
                st.success("MSE export completed (check modules/databases/mse_output).")

    with col_exp2:
        if st.button("Run Mongo Exporter (30 days)"):
            if MongoExporter is None:
                st.warning("MongoExporter class not found (modules.databases.examples.MongoDB.MongoDB).")
            else:
                MongoExporter().main()
                st.success("Mongo export completed (check modules/databases/mongo_output).")

    with col_exp3:
        if st.button("Run Firebase Exporter (30 days)"):
            if FirebaseExporter is None:
                st.warning("FirebaseExporter class not found (modules.databases.examples.Firebase.Firebase).")
            else:
                FirebaseExporter().main()
                st.success("Firebase export completed (check modules/databases/firebase_output).")

    with col_exp4:
        if st.button("Run Dynamo Exporter (30 days)"):
            if DynamoExporter is None:
                st.warning("DynamoExporter class not found (modules.databases.examples.DynamoDB.DynamoDB).")
            else:
                DynamoExporter().main()
                st.success("Dynamo export completed (check modules/databases/dynamodb_output).")

    with col_exp5:
        if st.button("Run SQL Exporter (30 days)"):
            if SQLExporter is None:
                st.warning("SQLExporter class not found (modules.databases.examples.MySQL.MySQL).")
            else:
                SQLExporter().main()
                st.success("SQL export completed (check modules/databases/sql_output).")


    st.markdown("---")
    st.caption("Morphic Semantic Engine • One seed → four databases → live storage savings.")


if __name__ == "__main__":
    main()

import hashlib
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. Routine "Personality" Traits & Storage Model
# ============================================================

ROUTINE_TRAITS = [
    "Morning Productivity",   # high = prefers deep work in morning
    "Evening Productivity",   # high = prefers deep work in evening
    "Fitness Focus",          # high = consistent exercise
    "Social / Family Focus",  # high = wants time with people
    "Learning / Growth",      # high = time for study/skills
    "Errands / Admin",        # high = structured chores/admin
    "Relaxation Priority",    # high = protects downtime
    "Weekend Warrior",        # high = shifts more to weekends
]

BYTES_PER_FLOAT = 4   # e.g. float32
BYTES_PER_CHAR = 1    # approx per character in seed string


@dataclass
class RoutineSeed:
    """Tiny, shareable representation of a daily routine style."""
    seed_code: str                # e.g. "R-9A23BC"
    vector: np.ndarray            # normalized trait vector (local only)
    raw_traits: Dict[str, float]  # original sliders (local only)


# ============================================================
# 2. Helper Functions
# ============================================================

def normalize_vector(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def hash_vector_to_code(prefix: str, v: np.ndarray) -> str:
    """Turn vector into a short deterministic seed code (demo-style)."""
    q = np.round(v * 100).astype(int)
    raw = ",".join(map(str, q.tolist())).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:6].upper()
    return f"{prefix}-{digest}"


def build_routine_seed(traits: Dict[str, float]) -> RoutineSeed:
    vec = np.array([traits[t] for t in ROUTINE_TRAITS], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("ROUT", vec_norm)
    return RoutineSeed(seed_code=seed_code, vector=vec_norm, raw_traits=traits)


def human_readable_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    kb = n / 1024
    if kb < 1024:
        return f"{kb:.1f} KB"
    mb = kb / 1024
    if mb < 1024:
        return f"{mb:.1f} MB"
    gb = mb / 1024
    if gb < 1024:
        return f"{gb:.1f} GB"
    tb = gb / 1024
    return f"{tb:.1f} TB"


# ============================================================
# 3. Routine Generation from RoutineSeed (Demo Logic)
# ============================================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def build_daily_routine(seed: RoutineSeed, is_weekend: bool) -> pd.DataFrame:
    """
    Generate a simple hourly schedule with intensities for:
      - deep_work (0-100)
      - fitness (0-100)
      - social_family (0-100)
      - admin_errands (0-100)
      - rest_relax (0-100)
    based on RoutineSeed traits.
    """

    traits = seed.raw_traits

    # 0–10 -> 0–1
    s = lambda name: traits[name] / 10.0

    morn = s("Morning Productivity")
    eve = s("Evening Productivity")
    fit = s("Fitness Focus")
    social = s("Social / Family Focus")
    learn = s("Learning / Growth")
    admin = s("Errands / Admin")
    relax = s("Relaxation Priority")
    weekend = s("Weekend Warrior")

    weekend_factor = weekend if is_weekend else 0.0

    hours = list(range(24))
    rows = []

    for h in hours:
        # Basic time windows
        is_morning = 6 <= h < 11
        is_midday = 11 <= h < 16
        is_evening = 16 <= h < 22
        is_night = (h >= 22 or h < 6)

        # Deep work
        deep = 0.0
        if is_morning:
            deep += 70 * morn
        if is_evening:
            deep += 70 * eve
        if is_midday:
            deep += 30 * (morn + eve) / 2.0
        # weekend factor: shift some deep work into weekend if weekend warrior
        deep *= (0.6 + 0.4 * (1.0 - weekend_factor))
        deep = clamp(deep, 0, 100)

        # Fitness: morning/evening + weekend boost
        fit_int = 0.0
        if 6 <= h < 9:
            fit_int += 60 * fit
        if 17 <= h < 20:
            fit_int += 50 * fit
        fit_int += 20 * weekend_factor * fit
        fit_int = clamp(fit_int, 0, 100)

        # Social/Family: evenings + weekend boost
        soc_int = 0.0
        if is_evening:
            soc_int += 60 * social
        if is_midday and is_weekend:
            soc_int += 40 * social
        soc_int += 20 * weekend_factor * social
        soc_int = clamp(soc_int, 0, 100)

        # Admin/Errands: midday + early evening
        adm_int = 0.0
        if 9 <= h < 12:
            adm_int += 50 * admin
        if 13 <= h < 17:
            adm_int += 40 * admin
        if is_weekend and 10 <= h < 14:
            adm_int += 20 * admin
        adm_int = clamp(adm_int, 0, 100)

        # Learning: often early morning, late evening, or midday blocks
        learn_int = 0.0
        if 6 <= h < 8:
            learn_int += 40 * learn
        if 20 <= h < 22:
            learn_int += 40 * learn
        if 12 <= h < 14:
            learn_int += 30 * learn
        learn_int = clamp(learn_int, 0, 100)

        # Rest / Relaxation: nights + free windows + driven by relax priority
        rest_int = 0.0
        if is_night:
            rest_int += 70
        if is_evening:
            rest_int += 30 * relax
        # subtract time already taken by other stuff
        busy = (deep + fit_int + soc_int + adm_int + learn_int) / 100.0
        rest_int += (1.0 - clamp(busy, 0.0, 1.0)) * 50 * relax
        rest_int = clamp(rest_int, 0, 100)

        rows.append(
            {
                "Hour": f"{h:02d}:00",
                "Deep Work (0-100)": round(deep, 1),
                "Fitness (0-100)": round(fit_int, 1),
                "Social / Family (0-100)": round(soc_int, 1),
                "Admin / Errands (0-100)": round(adm_int, 1),
                "Learning (0-100)": round(learn_int, 1),
                "Rest / Relax (0-100)": round(rest_int, 1),
            }
        )

    df = pd.DataFrame(rows)
    return df


# ============================================================
# 4. Storage & Bandwidth Estimates
# ============================================================

def estimate_storage_bytes_per_routine_profile(num_traits: int) -> int:
    """
    Assume you store one float per trait for the "routine personality".
    Schedules themselves could be derived on the fly from the seed.
    """
    return num_traits * BYTES_PER_FLOAT


def estimate_storage_bytes_per_routine_seed(seed_code: str) -> int:
    return len(seed_code) * BYTES_PER_CHAR


# ============================================================
# 5. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE Routine Planner Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE Routine Planner & Seed Compression Demo")

st.write(
    """
This demo shows how an **MSE-style RoutineSeed** can represent a person's
**daily planning style**, and how that saves **storage and bandwidth**.

- You control **routine traits** via sliders.
- The app builds a tiny **RoutineSeed** from those traits.
- That seed generates a **24-hour routine** (deep work, exercise, social, errands, rest).
- Then we estimate **storage/bandwidth savings** for seeds vs raw profiles.
"""
)

# Sidebar: traits
st.sidebar.header("🧑‍💼 Routine Traits")

st.sidebar.write("Set your routine tendencies (0 = not at all, 10 = very strong).")

default_traits = {
    "Morning Productivity": 7.0,
    "Evening Productivity": 4.0,
    "Fitness Focus": 5.0,
    "Social / Family Focus": 5.0,
    "Learning / Growth": 6.0,
    "Errands / Admin": 4.0,
    "Relaxation Priority": 5.0,
    "Weekend Warrior": 3.0,
}

trait_values: Dict[str, float] = {}
for trait in ROUTINE_TRAITS:
    trait_values[trait] = st.sidebar.slider(trait, 0.0, 10.0, float(default_traits[trait]), 0.5)

is_weekend = st.sidebar.checkbox("Generate weekend routine", value=False)
show_raw_profile = st.sidebar.checkbox("Show raw trait profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized routine vector (debug)", value=False)

# Build seed and schedule
routine_seed = build_routine_seed(trait_values)
routine_df = build_daily_routine(routine_seed, is_weekend=is_weekend)

# Layout columns
col_left, col_right = st.columns([1.1, 1.6])

with col_left:
    st.subheader("🧬 RoutineSeed & Preference Encoding")

    st.markdown(
        f"""
**Step 1 – Traits → RoutineSeed**

- The sliders define your **routine personality**:
  - when you're most productive,
  - how much you care about fitness,
  - how important social/family time is,
  - how structured your admin/errands time is,
  - how much you protect rest and relaxation.

- These traits become a **normalized vector**.
- That vector is encoded into a tiny seed:

> **RoutineSeed:** `{routine_seed.seed_code}`

In a full MSE system, this seed could regenerate:

- your preferred daily/weekly schedule,  
- task block templates,  
- focus vs shallow work balance,  
- how you adjust routines on weekends or busy days.

What you persist/sync is just the **seed**, not the full detailed schedule.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw traits (stay in the planner / on device):**")
        st.json(routine_seed.raw_traits)

    if show_vector:
        st.markdown("**Normalized routine vector:**")
        st.write(routine_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – From Seed to Daily Routine**

The engine uses the RoutineSeed to derive a **24-hour plan**:

- Deep work blocks  
- Exercise windows  
- Social/family time  
- Admin/errand blocks  
- Learning slots  
- Rest/relaxation

This demo uses simple heuristics; an actual MSE implementation would use
richer morphic rules and context-aware adjustments (meetings, travel, deadlines).
"""
    )

with col_right:
    st.subheader("📅 Generated Daily Routine (Hourly)")

    routine_type = "Weekend" if is_weekend else "Weekday"
    st.write(
        f"""
This table shows the **hour-by-hour routine** implied by the current RoutineSeed  
for a **{routine_type.lower()}** day. Tweak traits and watch the routine reshape itself. In real-world applications, these can be adjusted based on user preference.
"""
    )
    st.dataframe(routine_df, use_container_width=True)

    st.markdown(
        """
Examples:

- Increase **Morning Productivity** → more deep work in the morning hours.  
- Increase **Evening Productivity** → more deep work later in the day.  
- Increase **Fitness Focus** → stronger morning/evening exercise slots.  
- Increase **Social / Family Focus** → more evening and weekend social time.  
- Increase **Relaxation Priority** → more protected downtime, especially nights.
"""
    )

st.markdown("---")

# ============================================================
# 6. Storage & Bandwidth Savings
# ============================================================

st.subheader("💾 Storage & 📡 Bandwidth Savings for Routine Profiles")

# Per-user storage
raw_bytes_per_routine = estimate_storage_bytes_per_routine_profile(len(ROUTINE_TRAITS))
seed_bytes_per_routine = estimate_storage_bytes_per_routine_seed(routine_seed.seed_code)

st.markdown(
    f"""
### Per User

**Raw routine profile storage (traits only)**

- {len(ROUTINE_TRAITS)} traits × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_routine} bytes** per user

**Seed-only routine storage**

- `{routine_seed.seed_code}` → {len(routine_seed.seed_code)} characters × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_routine} bytes** per user

So in this simplified example, the seed is about **{raw_bytes_per_routine / max(seed_bytes_per_routine,1):.1f}× smaller**  
than storing the raw routine traits directly.

If you also encode template schedules, blocked tasks, and historical adjustments into the seed,
the savings get even bigger.
"""
)

# Scale for many users
scale_users = [1_000, 1_000_000, 100_000_000]
rows_storage = []
for n_users in scale_users:
    raw_total = raw_bytes_per_routine * n_users
    seed_total = seed_bytes_per_routine * n_users
    savings = 1.0 - (seed_total / raw_total) if raw_total > 0 else 0.0
    rows_storage.append(
        {
            "Users": f"{n_users:,}",
            "Raw Profile Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "Storage Saved": f"{savings*100:.1f}%",
        }
    )

st.markdown("### At Scale (Storage Across Many Users)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
Real routine planners can store:

- many custom routines,  
- daily logs,  
- completion history,  
- task metadata,  
- focus analytics.

If the MSE encodes most of the *pattern* into a **RoutineSeed (+ a few deltas)**,
you can sync routine intelligence everywhere (phone, desktop, watch) with minimal storage.
"""
)

# Bandwidth section
st.markdown("### Bandwidth Per Sync Across Devices")

st.markdown(
    """
Now imagine syncing your routine planner between:

- phone ↔ laptop,  
- laptop ↔ cloud,  
- cloud ↔ watch or tablet.

Instead of sending full profiles & schedules each time, you send:

- **RoutineSeed** (and occasional small updates),
- Let each device regenerate the daily/weekly view on its own.
"""
)

syncs_per_day = st.slider("Assumed routine syncs per user per day", 1, 200, 20)
users_in_system = st.slider("Number of users in the routine app", 10, 5_000_000, 100_000, step=10)

raw_payload_per_sync = raw_bytes_per_routine * users_in_system
seed_payload_per_sync = seed_bytes_per_routine * users_in_system
raw_per_day = raw_payload_per_sync * syncs_per_day
seed_per_day = seed_payload_per_sync * syncs_per_day
savings_per_day = 1.0 - (seed_per_day / raw_per_day) if raw_per_day > 0 else 0.0

rows_bandwidth = [
    {
        "Scenario": "Per sync",
        "Raw Profile Payload": human_readable_bytes(raw_payload_per_sync),
        "Seed Payload": human_readable_bytes(seed_payload_per_sync),
        "Bandwidth Saved": f"{(1 - seed_payload_per_sync / raw_payload_per_sync)*100:.1f}%" if raw_payload_per_sync > 0 else "0%",
    },
    {
        "Scenario": "Per day (all users)",
        "Raw Profile Payload": human_readable_bytes(int(raw_per_day)),
        "Seed Payload": human_readable_bytes(int(seed_per_day)),
        "Bandwidth Saved": f"{savings_per_day*100:.1f}%",
    },
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
With hundreds of thousands or millions of users, **seed-based routines**:

- keep storage light for long-term usage patterns,  
- reduce sync overhead for multi-device setups,  
- allow on-device planners to be smarter without constant heavy network calls.

This is the routine-planning version of:

> **Infinite personalized planning, finite tiny seeds.**
"""
)

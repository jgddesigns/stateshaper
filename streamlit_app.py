import hashlib
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. Smart Home "Personality" Traits & Storage Model
# ============================================================

HOME_TRAITS = [
    "Early Riser",        # high = early morning activity
    "Night Owl",          # high = late activity
    "Work From Home",     # high = home daytime occupancy
    "Energy Saving",      # high = prefers lower energy usage
    "Comfort Priority",   # high = stable temps, dim lights
    "Security Focus",     # high = more security events
    "Weekend Social",     # high = more evening activity weekends
    "Kids in Home",       # high = earlier lights, more schedule structure
]

BYTES_PER_FLOAT = 4   # e.g. float32 for scheduling parameters
BYTES_PER_CHAR = 1    # approximated per character in seed string


@dataclass
class HomeSeed:
    """Tiny, shareable representation of smart home behavior profile."""
    seed_code: str                # e.g. "HOME-9A23BC"
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


def build_home_seed(traits: Dict[str, float]) -> HomeSeed:
    vec = np.array([traits[t] for t in HOME_TRAITS], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("HOME", vec_norm)
    return HomeSeed(seed_code=seed_code, vector=vec_norm, raw_traits=traits)


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
# 3. Schedule Generation from HomeSeed (Demo Logic)
# ============================================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def build_daily_schedule(seed: HomeSeed) -> pd.DataFrame:
    """
    Generate a simple hourly schedule for:
      - lights (0-100)
      - thermostat temp (°F)
      - appliance activity (0-100)
      - security sensitivity (0-100)

    based on the HomeSeed traits.
    """

    traits = seed.raw_traits
    # Normalize slider 0–10 to 0–1
    s = lambda name: traits[name] / 10.0

    early = s("Early Riser")
    night = s("Night Owl")
    wfh = s("Work From Home")
    energy = s("Energy Saving")
    comfort = s("Comfort Priority")
    security = s("Security Focus")
    weekend = s("Weekend Social")
    kids = s("Kids in Home")

    hours = list(range(24))
    rows = []

    for h in hours:
        # Base occupancy probability curve
        if 6 <= h < 9:
            # morning
            occ_base = 0.5 + 0.5 * early
        elif 9 <= h < 17:
            # day
            occ_base = 0.2 + 0.6 * wfh
        elif 17 <= h < 22:
            # evening prime time
            occ_base = 0.4 + 0.5 * (night + weekend) / 2.0 + 0.1 * kids
        else:
            # night
            occ_base = 0.1 + 0.4 * night - 0.3 * early
        occ = clamp(occ_base, 0.0, 1.0)

        # Lights: more when occupancy + kids + evening or dark hours
        is_dark = (h < 7 or h >= 19)
        lights = 0.0
        lights += 70 * occ
        if is_dark:
            lights += 20
        lights += 10 * kids
        lights *= (0.6 + 0.4 * comfort)   # comfort amplifies lights
        lights *= (1.0 - 0.3 * energy)    # energy saving reduces lights
        lights = clamp(lights, 0, 100)

        # Thermostat: base comfortable range: 70°F ± 6
        # comfort = likes it stable and cozy
        # energy saving = allows larger swings
        base_temp = 70.0
        # Variation by time (cooler at night, warmer in evening)
        temp_variation = 0.0
        if 0 <= h < 6:
            temp_variation = -2.0
        elif 6 <= h < 9:
            temp_variation = 0.0
        elif 9 <= h < 17:
            temp_variation = -1.0
        elif 17 <= h < 22:
            temp_variation = 1.0
        else:
            temp_variation = -1.5

        # Comfort = keep near base; energy = allow bigger drops at night
        temp = base_temp + temp_variation
        temp -= 3.0 * energy * (1.0 - comfort)  # more energy saving, less comfort => cooler
        temp = clamp(temp, 62, 78)

        # Appliances: cooking, laundry, dishwasher, etc.
        # More active mornings & evenings, especially with kids or weekend social.
        app = 0.0
        if 7 <= h < 9:
            app += 50  # breakfast window
        if 17 <= h < 21:
            app += 60  # dinner/evening
        app += 20 * kids
        app += 30 * weekend
        app *= occ
        app *= (1.0 - 0.5 * energy)  # energy saving reduces appliance use
        app = clamp(app, 0, 100)

        # Security sensitivity: higher when home is empty, or at night, or security focused.
        empty_factor = (1.0 - occ)
        sec = 40 * empty_factor + 30 * security
        if h < 6 or h >= 22:
            sec += 20  # nights
        sec = clamp(sec, 0, 100)

        rows.append(
            {
                "Hour": f"{h:02d}:00",
                "Occupancy (0-100)": round(occ * 100, 1),
                "Lights (0-100)": round(lights, 1),
                "Thermostat (°F)": round(temp, 1),
                "Appliances (0-100)": round(app, 1),
                "Security Sensitivity (0-100)": round(sec, 1),
            }
        )

    df = pd.DataFrame(rows)
    return df


# ============================================================
# 4. Storage & Bandwidth Estimates
# ============================================================

def estimate_storage_bytes_per_home_profile(num_traits: int, schedule_length: int) -> int:
    """
    Assume:
    - raw traits: num_traits floats
    - schedule: for each hour a few floats (lights, temp, etc.)
    For the demo, we only show trait side in detail, but we can
    count schedule as additional floats if desired.
    """
    # traits only here; you can add schedule floats if you want it stricter
    return num_traits * BYTES_PER_FLOAT


def estimate_storage_bytes_per_home_seed(seed_code: str) -> int:
    return len(seed_code) * BYTES_PER_CHAR


# ============================================================
# 5. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE Smart Home Scheduling Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE Smart Home Scheduling & Seed Compression Demo")

st.write(
    """
This demo shows how an **MSE-style seed** can represent a home's
**behavior & schedule preferences**, and how that saves **storage and bandwidth**.

- You control a **smart home personality** (traits) via sliders.
- The app builds a tiny **HomeSeed** from those traits.
- That seed generates a **daily smart home schedule** (lights, thermostat, appliances, security).
- We then estimate **storage/bandwidth savings** for seeds vs raw profiles.
"""
)

# Sidebar: traits
st.sidebar.header("🏠 Smart Home Traits")

st.sidebar.write("Set the home's behavior tendencies (0 = not at all, 10 = very strong).")

default_traits = {
    "Early Riser": 6.0,
    "Night Owl": 4.0,
    "Work From Home": 7.0,
    "Energy Saving": 5.0,
    "Comfort Priority": 6.0,
    "Security Focus": 5.0,
    "Weekend Social": 3.0,
    "Kids in Home": 5.0,
}

trait_values: Dict[str, float] = {}
for trait in HOME_TRAITS:
    trait_values[trait] = st.sidebar.slider(trait, 0.0, 10.0, float(default_traits[trait]), 0.5)

show_raw_profile = st.sidebar.checkbox("Show raw trait profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized preference vector (debug)", value=False)

# Build seed and schedule
home_seed = build_home_seed(trait_values)
schedule_df = build_daily_schedule(home_seed)

# Layout columns
col_left, col_right = st.columns([1.1, 1.6])

with col_left:
    st.subheader("🧬 HomeSeed & Preference Encoding")

    st.markdown(
        f"""
**Step 1 – Traits → HomeSeed**

- The sliders define the home's **behavior traits**:
  - when people are active,
  - how much they value energy saving vs comfort,
  - how security-conscious they are,
  - how kid-focused / structured the schedule is.

- These traits become a **normalized vector**.
- That vector is encoded into a tiny seed:

> **HomeSeed:** `{home_seed.seed_code}`

In a full MSE system, the seed would be enough to regenerate:

- preferred lighting patterns,  
- thermostat automation rules,  
- appliance usage windows,  
- security sensitivity curves,  
- and even adaptive policies over days/seasons.

But what you store/transmit is just the **seed**, not the full profile.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw traits (stay in app / on device):**")
        st.json(home_seed.raw_traits)

    if show_vector:
        st.markdown("**Normalized preference vector:**")
        st.write(home_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – From Seed to Daily Schedule**

The engine uses the HomeSeed to derive a **24-hour schedule** for:

- occupancy likelihood,  
- lighting level,  
- thermostat setpoint,  
- appliance activity,  
- security sensitivity.

This demo uses simple heuristics, but the real MSE would use
more complex morphic functions and learned behaviors.
"""
    )

with col_right:
    st.subheader("📅 Generated Daily Smart Home Schedule (Hourly)")

    st.write(
        """
This table shows the **hour-by-hour behavior** implied by the current HomeSeed.
You can tweak traits and immediately see how the schedule responds. In real-world applications, these values can be adjusted over time as inhabitant use changes. 
"""
    )
    st.dataframe(schedule_df, use_container_width=True)

    st.markdown(
        """
Examples:

- Increase **Early Riser** → earlier occupancy & lights.  
- Increase **Work From Home** → more daytime occupancy and appliance usage.  
- Increase **Energy Saving** → lower light levels & cooler temps.  
- Increase **Security Focus** → higher security sensitivity when the home is empty or at night.
"""
    )

st.markdown("---")

# ============================================================
# 6. Storage & Bandwidth Savings
# ============================================================

st.subheader("💾 Storage & 📡 Bandwidth Savings for Smart Home Profiles")

# Per-home storage
raw_bytes_per_home = estimate_storage_bytes_per_home_profile(len(HOME_TRAITS), schedule_length=24)
seed_bytes_per_home = estimate_storage_bytes_per_home_seed(home_seed.seed_code)

st.markdown(
    f"""
### Per Home

**Raw behavior profile storage (traits only)**

- {len(HOME_TRAITS)} traits × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_home} bytes** per home

**Seed-only behavior storage**

- `{home_seed.seed_code}` → {len(home_seed.seed_code)} characters × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_home} bytes** per home

So in this simplified example, the seed is about **{raw_bytes_per_home / max(seed_bytes_per_home,1):.1f}× smaller**  
than storing the raw trait profile directly.

If you also encoded schedules, routines, scenes, and learned behaviors into the seed,
the savings multiply further.
"""
)

# Scale for many homes
scale_homes = [1_000, 1_000_000, 100_000_000]
rows_storage = []
for n_homes in scale_homes:
    raw_total = raw_bytes_per_home * n_homes
    seed_total = seed_bytes_per_home * n_homes
    savings = 1.0 - (seed_total / raw_total) if raw_total > 0 else 0.0
    rows_storage.append(
        {
            "Homes": f"{n_homes:,}",
            "Raw Profile Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "Storage Saved": f"{savings*100:.1f}%",
        }
    )

st.markdown("### At Scale (Storage Across Many Homes)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
Real smart home systems may store:

- multiple daily/weekly schedules per device,  
- logs of occupancy/activity,  
- per-room preferences,  
- historical patterns for learning.

If the MSE encodes much of that into a **single HomeSeed (+ a few deltas)**,
you compress *years* of behavior into something small enough to sync anywhere.
"""
)

# Bandwidth section
st.markdown("### Bandwidth Per Sync / Cloud Round Trip")

st.markdown(
    """
Now imagine syncing behavior between:

- Phone app ↔ Smart home hub,  
- Hub ↔ Cloud AI model,  
- Multiple hubs in a multi-property setup.

Instead of shipping full profiles and schedules, you can ship:

- **HomeSeed** (and occasionally small updates),
- Let each side regenerate the behavior model when needed.
"""
)

syncs_per_day = st.slider("Assumed behavior syncs per home per day", 1, 200, 20)
homes_in_network = st.slider("Number of homes in network", 10, 5_000_000, 50_000, step=10)

raw_payload_per_sync = raw_bytes_per_home * homes_in_network
seed_payload_per_sync = seed_bytes_per_home * homes_in_network
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
        "Scenario": "Per day (all homes)",
        "Raw Profile Payload": human_readable_bytes(int(raw_per_day)),
        "Seed Payload": human_readable_bytes(int(seed_per_day)),
        "Bandwidth Saved": f"{savings_per_day*100:.1f}%",
    },
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
With thousands or millions of homes, **seed-based behavior modeling**:

- cuts storage for historical behavior/schedules,  
- slashes bandwidth for sync and AI updates,  
- lets you move intelligence to the edge (on-device HomeSeed),  
- and still allows sophisticated, personalized automation.

This is the smart-home version of:

> **Infinite personalized scheduling, finite tiny seeds.**
"""
)

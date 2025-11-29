import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. Simple "MSE-style" Seed Structures for the Demo
# ============================================================

CATEGORIES = ["Sports", "Tech", "Travel", "Fashion", "Food", "Finance", "Gaming", "Health"]

# Storage model assumptions (rough, illustrative)
BYTES_PER_FLOAT = 8       # double precision float
BYTES_PER_CHAR = 1        # approx per character in seed string


@dataclass
class UserSeed:
    """Tiny, shareable representation of a user profile."""
    seed_code: str          # e.g. "U-3F9A2C"
    vector: np.ndarray      # normalized preference vector (local only)
    raw_profile: Dict[str, float]  # original slider values (local only)


@dataclass
class AdSeed:
    """Tiny, shareable representation of an ad profile."""
    ad_id: str
    name: str
    category_focus: Dict[str, float]      # human-readable
    vector: np.ndarray                    # normalized category vector
    seed_code: str                        # e.g. "AD-912C01"


# ============================================================
# 2. Helper Functions
# ============================================================

def normalize_vector(v: np.ndarray) -> np.ndarray:
    """Normalize vector to unit length; if zero, return zero vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def hash_vector_to_code(prefix: str, v: np.ndarray) -> str:
    """
    Turn a numeric vector into a short deterministic seed code.
    In a real MSE, this would be a proper seed; here it's a simple hash.
    """
    # Quantize vector a bit to keep stable-ish across small noise
    q = np.round(v * 100).astype(int)
    raw = ",".join(map(str, q.tolist())).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:6].upper()
    return f"{prefix}-{digest}"


def build_user_seed(slider_values: Dict[str, float]) -> UserSeed:
    """Create a UserSeed from category slider values."""
    vec = np.array([slider_values[cat] for cat in CATEGORIES], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("U", vec_norm)
    return UserSeed(seed_code=seed_code, vector=vec_norm, raw_profile=slider_values)


def build_ad_seeds() -> List[AdSeed]:
    """Create a small catalog of demo ads with category weights."""
    ads_raw = [
        ("AD1", "UltraFit Running Shoes",   {"Sports": 0.9, "Health": 0.6, "Fashion": 0.3}),
        ("AD2", "4K Gaming Laptop",         {"Tech": 0.9, "Gaming": 0.9, "Finance": 0.2}),
        ("AD3", "Budget Travel Package",    {"Travel": 0.9, "Food": 0.4}),
        ("AD4", "Organic Meal Kit",         {"Food": 0.9, "Health": 0.7}),
        ("AD5", "Crypto Investing Course",  {"Finance": 0.9, "Tech": 0.4}),
        ("AD6", "Yoga & Wellness App",      {"Health": 0.9, "Sports": 0.3}),
        ("AD7", "Streetwear Hoodie Drop",   {"Fashion": 0.9, "Gaming": 0.3}),
        ("AD8", "Noise-Cancelling Headphones", {"Tech": 0.8, "Travel": 0.4}),
        ("AD9", "Gourmet Food Delivery",    {"Food": 0.9}),
        ("AD10", "Adventure Travel Insurance", {"Travel": 0.7, "Finance": 0.5}),
    ]

    ad_seeds: List[AdSeed] = []
    for ad_id, name, cats in ads_raw:
        vec = np.array([cats.get(cat, 0.0) for cat in CATEGORIES], dtype=float)
        vec_norm = normalize_vector(vec)
        seed_code = hash_vector_to_code("AD", vec_norm)
        ad_seeds.append(
            AdSeed(
                ad_id=ad_id,
                name=name,
                category_focus=cats,
                vector=vec_norm,
                seed_code=seed_code,
            )
        )
    return ad_seeds


def compatibility_score(user_vec: np.ndarray, ad_vec: np.ndarray) -> float:
    """
    Simple similarity measure between user and ad seeds.
    Here: cosine similarity in [0,1].
    In a real MSE: more complex morphing logic based on seeds.
    """
    if np.linalg.norm(user_vec) == 0 or np.linalg.norm(ad_vec) == 0:
        return 0.0
    cos = float(np.dot(user_vec, ad_vec))
    # cos is already in [0,1] because vectors are normalized and non-negative
    return cos


# ============================================================
# 3. Storage & Bandwidth Estimation Helpers
# ============================================================

def estimate_storage_bytes_per_user_profile(num_categories: int) -> int:
    """
    Estimate bytes for storing a raw profile: one float per category.
    Very simplified: num_categories * BYTES_PER_FLOAT.
    """
    return num_categories * BYTES_PER_FLOAT


def estimate_storage_bytes_per_user_seed(seed_code: str) -> int:
    """
    Estimate bytes for storing just the seed string.
    Again, simplified: one byte per character.
    """
    return len(seed_code) * BYTES_PER_CHAR


def human_readable_bytes(n: int) -> str:
    """Format bytes into KB/MB/GB nicely."""
    if n < 1024:
        return f"{n} B"
    kb = n / 1024
    if kb < 1024:
        return f"{kb:.1f} KB"
    mb = kb / 1024
    if mb < 1024:
        return f"{mb:.1f} MB"
    gb = mb / 1024
    return f"{gb:.1f} GB"


# ============================================================
# 4. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE Targeted Advertising Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE Targeted Advertising Demo")
st.write(
    """
This demo shows *how an MSE-style seed can be used for targeted advertising* —  
**and** how much **storage and bandwidth** can be saved by using seeds instead of full profiles.

- You control a **user's interests** via sliders (this is the **raw profile**, kept local).
- The app compresses those interests into a tiny **UserSeed** (a short code).
- Each ad has its own **AdSeed**.
- The system only needs the **seeds** (not the detailed profile) to compute relevance.
"""
)

# ------------------------------------------------------------
# Sidebar: user interest sliders
# ------------------------------------------------------------
st.sidebar.header("🧑 User Interest Profile")

st.sidebar.write("Set how much this user cares about each category (0 = not at all, 10 = very interested).")

default_values = {
    "Sports": 3.0,
    "Tech": 8.0,
    "Travel": 5.0,
    "Fashion": 2.0,
    "Food": 7.0,
    "Finance": 4.0,
    "Gaming": 6.0,
    "Health": 5.0,
}

slider_values: Dict[str, float] = {}
for cat in CATEGORIES:
    slider_values[cat] = st.sidebar.slider(cat, 0.0, 10.0, float(default_values[cat]), 0.5)

show_raw_profile = st.sidebar.checkbox("Show detailed profile (local only)", value=True)
show_vectors = st.sidebar.checkbox("Show raw seed vectors (debug)", value=False)

# ------------------------------------------------------------
# Build seeds and compute matches
# ------------------------------------------------------------
user_seed = build_user_seed(slider_values)
ads = build_ad_seeds()

rows = []
for ad in ads:
    score = compatibility_score(user_seed.vector, ad.vector)
    rows.append(
        {
            "Ad ID": ad.ad_id,
            "Ad Name": ad.name,
            "Match Score (0–100)": round(score * 100, 1),
            "Ad Seed": ad.seed_code,
        }
    )

df = pd.DataFrame(rows).sort_values(by="Match Score (0–100)", ascending=False).reset_index(drop=True)

# ------------------------------------------------------------
# Layout: left = explanation, right = results
# ------------------------------------------------------------
col_left, col_right = st.columns([1.1, 1.4])

with col_left:
    st.subheader("🎯 What the MSE is doing here")

    st.markdown(
        f"""
**Step 1 – User profile → UserSeed**

- Your sliders (one per category) define the **raw interest profile**.
- That profile is turned into a **normalized vector**.
- The vector is hashed/encoded as a tiny seed:  
  `UserSeed: `{user_seed.seed_code}`

In a *real* MSE system, this seed would be enough to:
- Recreate a rich behavioral profile,
- Predict future interests,
- Generate synthetic lookalike behavior.

But what gets shared with the ad system is only the **seed**, *not* the raw sliders.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw profile (stays on device):**")
        st.json(user_seed.raw_profile)

    if show_vectors:
        st.markdown("**User vector (normalized):**")
        st.write(user_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – Ads → AdSeeds**

Each ad is also encoded as:
- a category vector (what kind of user it targets),
- a tiny `AdSeed` code.

The system compares **UserSeed ↔ AdSeed** to compute a relevance score.
"""
    )

    if show_vectors:
        st.markdown("**Ad vectors (normalized):**")
        debug_rows = []
        for ad in ads:
            debug_rows.append(
                {
                    "Ad ID": ad.ad_id,
                    "Ad Name": ad.name,
                    "Seed": ad.seed_code,
                    "Vector": ad.vector,
                }
            )
        st.dataframe(pd.DataFrame(debug_rows))


with col_right:
    st.subheader("📈 Ranked Ads by Match Score")

    st.write(
        f"""
Using only **UserSeed = `{user_seed.seed_code}`** and each **AdSeed**,  
the engine computes a **match score** (0–100) that estimates how relevant an ad is for this user.
"""
    )

    st.dataframe(df, use_container_width=True)

    st.markdown(
        """
Top-ranked ads are those whose **category focus** most closely matches the user's interest pattern.

In a full MSE system:
- The seeds would be far more expressive (behavior over time, spending curves, context),
- The matching function would be a complex morphic equation instead of a simple cosine,
- The same tiny seeds could also power **recommendations, simulations, and forecasting**.
"""
    )

st.markdown("---")

# ------------------------------------------------------------
# Storage & Bandwidth Savings Section
# ------------------------------------------------------------
st.subheader("💾 Storage & 📡 Bandwidth Savings With Seeds")

# Per-user storage estimates
raw_bytes_per_user = estimate_storage_bytes_per_user_profile(len(CATEGORIES))
seed_bytes_per_user = estimate_storage_bytes_per_user_seed(user_seed.seed_code)

st.markdown(
    f"""
### Per User

**Raw profile storage**  
- {len(CATEGORIES)} categories × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_user} bytes** per user

**Seed-only storage**  
- `{user_seed.seed_code}` → {len(user_seed.seed_code)} characters × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_user} bytes** per user

So for this demo profile, the seed is about **{raw_bytes_per_user / max(seed_bytes_per_user,1):.1f}× smaller** than the raw numeric profile.
"""
)

# Scale it up to many users
scale_users = [1_000, 1_000_000, 100_000_000]
rows_storage = []
for n_users in scale_users:
    raw_total = raw_bytes_per_user * n_users
    seed_total = seed_bytes_per_user * n_users
    savings = 1.0 - (seed_total / raw_total) if raw_total > 0 else 0.0
    rows_storage.append(
        {
            "Users": f"{n_users:,}",
            "Raw Profile Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "Storage Saved": f"{savings*100:.1f}%",
        }
    )

st.markdown("### At Scale (Storage for Many Users)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
This is just the *user profile* side. In real systems, profiles can include:

- dozens to hundreds of features,  
- time histories,  
- cross-device identifiers,  
- and model-specific embeddings.

Replacing that bulk with a **single MSE seed per user** multiplies these savings.
"""
)

# Bandwidth estimates per ad request
st.markdown("### Bandwidth Per Ad Request")

st.markdown(
    """
Imagine each ad request from a device to an ad server:

- **Traditional**: send full profile (or large identifier that maps to a heavy profile in the cloud).  
- **MSE-style**: send only the `UserSeed` string.

We’ll compare the payload if we:
- send **raw profile values** vs
- send just the **UserSeed**.
"""
)

# Assume one impression = send profile / send seed
impressions_per_day = [10_000, 1_000_000, 100_000_000]

rows_bandwidth = []
for n in impressions_per_day:
    raw_payload = raw_bytes_per_user * n
    seed_payload = seed_bytes_per_user * n
    savings = 1.0 - (seed_payload / raw_payload) if raw_payload > 0 else 0.0
    rows_bandwidth.append(
        {
            "Daily Ad Impressions": f"{n:,}",
            "Raw Profile Bandwidth": human_readable_bytes(raw_payload),
            "Seed-Only Bandwidth": human_readable_bytes(seed_payload),
            "Bandwidth Saved": f"{savings*100:.1f}%",
        }
    )

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
In practice, seeds can be:

- encoded as compact binary instead of strings,  
- combined for multiple tasks (ads, recommendations, analytics),  
- updated in-place rather than sending full fresh profiles each time.

The result is **huge bandwidth savings**, especially on mobile networks and high-traffic platforms.
"""
)

st.markdown("---")

st.subheader("🔒 Privacy & Efficiency Story")

st.markdown(
    """
- **Raw user data** (sliders, logs, history) can stay on-device or in a protected store.
- A tiny **UserSeed** is shared with the ad infrastructure instead of the full profile.
- That same seed can be reused across:
  - ad targeting,  
  - recommendations,  
  - synthetic audience simulations,  
  - forecasting.

This is where the MSE shines:

> One compact seed → many high-value behaviors and predictions,  
> without repeatedly shipping or storing the full underlying data.
"""
)

import hashlib
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. Simple "MSE-style" NPC Seed Structures
# ============================================================

NPC_TRAITS = [
    "Aggression",
    "Curiosity",
    "Loyalty",
    "Greed",
    "Wisdom",
    "Bravery",
    "Playfulness",
    "Patience",
]

# Storage model assumptions (rough, illustrative)
BYTES_PER_FLOAT = 4       # e.g. float32 for game state
BYTES_PER_CHAR = 1        # approx per character in seed string


@dataclass
class NPCSeed:
    """Tiny, shareable representation of an NPC behavior profile."""
    seed_code: str                # e.g. "NPC-8FA12C"
    vector: np.ndarray            # normalized trait vector (local only)
    raw_traits: Dict[str, float]  # original slider values (local only)


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
    In a real MSE, this would be a proper morphic seed; here it's a simple hash.
    """
    q = np.round(v * 100).astype(int)  # quantize for stability
    raw = ",".join(map(str, q.tolist())).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:6].upper()
    return f"{prefix}-{digest}"


def build_npc_seed(traits: Dict[str, float]) -> NPCSeed:
    """Create an NPCSeed from trait slider values."""
    vec = np.array([traits[t] for t in NPC_TRAITS], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("NPC", vec_norm)
    return NPCSeed(seed_code=seed_code, vector=vec_norm, raw_traits=traits)


# ============================================================
# 3. Behavior Tendencies (demo logic)
# ============================================================

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def compute_behavior_tendencies(seed: NPCSeed) -> pd.DataFrame:
    """
    Map trait vector to a few demo behaviors with likelihood scores.
    This is just illustrative; in a real MSE you'd morph the seed
    into a complex behavior policy or state machine.
    """
    # Pull traits in a stable order
    traits = seed.raw_traits
    aggr = traits["Aggression"]
    curi = traits["Curiosity"]
    loy  = traits["Loyalty"]
    greed = traits["Greed"]
    wis   = traits["Wisdom"]
    brav  = traits["Bravery"]
    play  = traits["Playfulness"]
    pat   = traits["Patience"]

    # Scale 0–10 sliders to 0–1
    def s(x): return x / 10.0

    # Simple heuristic scores for demo behaviors
    behaviors = []

    attack_score = clamp01(0.6 * s(aggr) + 0.4 * s(brav) - 0.3 * s(pat))
    behaviors.append(("Attack on sight", attack_score))

    trade_score = clamp01(0.5 * s(greed) + 0.5 * s(curi) - 0.2 * s(aggr))
    behaviors.append(("Offer trade", trade_score))

    help_score = clamp01(0.5 * s(loy) + 0.5 * s(wis) - 0.3 * s(greed))
    behaviors.append(("Offer help / quest hint", help_score))

    joke_score = clamp01(0.7 * s(play) + 0.2 * s(curi) - 0.2 * s(aggr))
    behaviors.append(("Tell a joke / banter", joke_score))

    avoid_score = clamp01(0.6 * s(pat) + 0.4 * s(wis) - 0.4 * s(aggr))
    behaviors.append(("Avoid conflict / flee", avoid_score))

    sneak_score = clamp01(0.5 * s(brav) + 0.3 * s(curi) + 0.2 * s(greed) - 0.3 * s(pat))
    behaviors.append(("Sneak / ambush", sneak_score))

    # Build DataFrame
    rows = [
        {
            "Behavior": name,
            "Likelihood (0–100)": round(score * 100, 1),
        }
        for name, score in behaviors
    ]
    df = pd.DataFrame(rows).sort_values(by="Likelihood (0–100)", ascending=False).reset_index(drop=True)
    return df


# ============================================================
# 4. Storage & Bandwidth Estimation Helpers
# ============================================================

def estimate_storage_bytes_per_npc_profile(num_traits: int) -> int:
    """
    Estimate bytes for storing a raw NPC behavior profile:
    one float per trait (very simplified).
    """
    return num_traits * BYTES_PER_FLOAT


def estimate_storage_bytes_per_npc_seed(seed_code: str) -> int:
    """
    Estimate bytes for storing just the seed string
    (could be much smaller with a binary encoding).
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
    if gb < 1024:
        return f"{gb:.1f} GB"
    tb = gb / 1024
    return f"{tb:.1f} TB"


# ============================================================
# 5. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE NPC Behavior Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE NPC Behavior & Seed Compression Demo")

st.write(
    """
This demo shows how an **MSE-style NPC seed** can:

- Encode an NPC's **behavior personality** into a tiny code,  
- Drive **behavior tendencies** (attack, trade, help, joke, flee, etc.),  
- Dramatically reduce **storage & bandwidth** compared to raw behavior profiles.

Think of this as a simplified example of:

> **Full behavior model → tiny deterministic seed → regenerated on demand.**
"""
)

# ------------------------------------------------------------
# Sidebar: NPC behavior trait sliders
# ------------------------------------------------------------
st.sidebar.header("🧍 NPC Behavior Traits")

st.sidebar.write("Set this NPC's tendencies (0 = not at all, 10 = very strong).")

default_traits = {
    "Aggression": 4.0,
    "Curiosity": 6.0,
    "Loyalty": 5.0,
    "Greed": 3.0,
    "Wisdom": 5.0,
    "Bravery": 7.0,
    "Playfulness": 4.0,
    "Patience": 3.0,
}

trait_values: Dict[str, float] = {}
for trait in NPC_TRAITS:
    trait_values[trait] = st.sidebar.slider(trait, 0.0, 10.0, float(default_traits[trait]), 0.5)

show_raw_profile = st.sidebar.checkbox("Show raw trait profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized behavior vector (debug)", value=False)

# ------------------------------------------------------------
# Build NPC seed and behavior tendencies
# ------------------------------------------------------------
npc_seed = build_npc_seed(trait_values)
behavior_df = compute_behavior_tendencies(npc_seed)

# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------
col_left, col_right = st.columns([1.1, 1.4])

with col_left:
    st.subheader("🧬 NPCSeed & Behavior Encoding")

    st.markdown(
        f"""
**Step 1 – Traits → NPCSeed**

- The sliders define the NPC's **behavior traits**.
- Traits are converted into a normalized vector.
- That vector is encoded into a tiny seed:

> **NPCSeed:** `{npc_seed.seed_code}`

In a full MSE implementation, this seed would be enough to regenerate:

- Personality curves,
- Response scripts,
- State machine parameters,
- Even synthetic dialogue or routines.

But what would be stored/transmitted is just the **seed**, not the full trait profile.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw traits (stay in memory / editor only):**")
        st.json(npc_seed.raw_traits)

    if show_vector:
        st.markdown("**Normalized behavior vector (for engine):**")
        st.write(npc_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – From Seed to Behavior Tendencies**

The engine uses the seed's vector to estimate how likely the NPC is to:

- attack,
- trade,
- help,
- crack a joke,
- avoid conflict,
- or attempt a sneak/ambush.

This is just a simple scoring function for the demo; in a real system, the
MSE would morph the seed into more complex behavior policies or scripts.
"""
    )

with col_right:
    st.subheader("🎭 Behavior Tendencies (Demo)")

    st.write(
        """
These are **derived behaviors** from the current NPCSeed. Scores can be mapped to event functions and modified as the game progresses. Higher scores mean the NPC is more likely to choose that behavior in encounters.
"""
    )

    st.dataframe(behavior_df, use_container_width=True)

    st.markdown(
        """
You can quickly prototype NPC types:

- High **Aggression + Bravery** → more likely to attack or ambush.
- High **Loyalty + Wisdom** → more helpful, less greedy.
- High **Playfulness + Curiosity** → more jokes, more trade, less violence.
"""
    )

st.markdown("---")

# ============================================================
# 6. Storage & Bandwidth Savings
# ============================================================

st.subheader("💾 Storage & 📡 Bandwidth Savings for NPCs")

# Per-NPC storage estimates
raw_bytes_per_npc = estimate_storage_bytes_per_npc_profile(len(NPC_TRAITS))
seed_bytes_per_npc = estimate_storage_bytes_per_npc_seed(npc_seed.seed_code)

st.markdown(
    f"""
### Per NPC

**Raw behavior profile storage**

- {len(NPC_TRAITS)} traits × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_npc} bytes** per NPC

**Seed-only behavior storage**

- `{npc_seed.seed_code}` → {len(npc_seed.seed_code)} characters × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_npc} bytes** per NPC

So for this example, the seed is about **{raw_bytes_per_npc / max(seed_bytes_per_npc,1):.1f}× smaller**  
than storing the raw traits directly.
"""
)

# Scale up to many NPCs
scale_npcs = [1_000, 1_000_000, 100_000_000]
rows_storage = []
for n_npcs in scale_npcs:
    raw_total = raw_bytes_per_npc * n_npcs
    seed_total = seed_bytes_per_npc * n_npcs
    savings = 1.0 - (seed_total / raw_total) if raw_total > 0 else 0.0
    rows_storage.append(
        {
            "NPCs": f"{n_npcs:,}",
            "Raw Profile Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "Storage Saved": f"{savings*100:.1f}%",
        }
    )

st.markdown("### At Scale (Storage for Many NPCs)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
In a real game, an NPC’s full state might include:

- stats,  
- skills,  
- equipment,  
- long-term memory,  
- schedule,  
- relationships,  

and more.

If the MSE can encode much of that into a small **behavior seed + a few extra parameters**,  
you multiply these storage savings across your entire world.
"""
)

# Bandwidth estimates per update
st.markdown("### Bandwidth Per NPC Update / Replication")

st.markdown(
    """
Now imagine syncing NPC behavior across:

- client ↔ server,  
- shards, or  
- save/load systems.

Instead of sending the whole behavior profile every time, you can send just:

- the **NPCSeed**, or  
- a seed + tiny delta updates.

Below is a rough comparison of sending the full trait vector vs just the seed.
"""
)

updates_per_second = st.slider("Assumed NPC updates per second (for replication)", 1, 60, 10)
npcs_in_scene = st.slider("Number of active NPCs in scene", 10, 10_000, 500, 10)

# bandwidth per update step
raw_payload_per_step = raw_bytes_per_npc * npcs_in_scene
seed_payload_per_step = seed_bytes_per_npc * npcs_in_scene
raw_per_second = raw_payload_per_step * updates_per_second
seed_per_second = seed_payload_per_step * updates_per_second
savings_per_second = 1.0 - (seed_per_second / raw_per_second) if raw_per_second > 0 else 0.0

rows_bandwidth = [
    {
        "Scenario": "Per update step",
        "Raw Behavior Payload": human_readable_bytes(raw_payload_per_step),
        "Seed Payload": human_readable_bytes(seed_payload_per_step),
        "Bandwidth Saved": f"{(1 - seed_payload_per_step / raw_payload_per_step)*100:.1f}%" if raw_payload_per_step > 0 else "0%",
    },
    {
        "Scenario": "Per second",
        "Raw Behavior Payload": human_readable_bytes(int(raw_per_second)),
        "Seed Payload": human_readable_bytes(int(seed_per_second)),
        "Bandwidth Saved": f"{savings_per_second*100:.1f}%",
    },
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
With hundreds or thousands of NPCs:

- Seed-based syncing greatly reduces bandwidth for **multiplayer**,  
- Makes cross-platform or cloud streaming more efficient,  
- And allows NPC behavior to be **regenerated deterministically** on each client.

You can even keep most behavior logic on the client, with the server only
sending **seed updates** or **seed morphs** when the NPC evolves.
"""
)

st.markdown("---")

st.subheader("🔚 Summary")

st.markdown(
    """
- The **NPCSeed** is a compact, deterministic handle on rich behavior.  
- It supports both **procedural generation** and **state compression**.  
- Storage and bandwidth savings scale massively with world size.  

This is exactly where an **MSE-based NPC system** shines:

> **Infinite-feeling behavior, finite tiny seeds.**
"""
)

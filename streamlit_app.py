import hashlib
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. ML Training "Personality" Traits & Storage Model
# ============================================================

TRAINING_TRAITS = [
    "Data Richness Preference",     # high = wants large datasets
    "Accuracy Priority",            # high = maximize metrics
    "Training Speed Priority",      # high = finish quickly
    "Regularization Strength",      # high = more reg
    "Augmentation Intensity",       # high = heavy aug
    "Experimentation Breadth",      # high = many runs/sweeps
    "On-Device / Edge Focus",       # high = smaller/lighter models
    "Interpretability Priority",    # high = simpler models, logs
]

BYTES_PER_FLOAT = 4   # e.g. float32 for config values
BYTES_PER_CHAR = 1    # approx per character in seed string


@dataclass
class TrainingSeed:
    """Tiny, shareable representation of an ML training style."""
    seed_code: str                # e.g. "ML-9A23BC"
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


def build_training_seed(traits: Dict[str, float]) -> TrainingSeed:
    vec = np.array([traits[t] for t in TRAINING_TRAITS], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("ML", vec_norm)
    return TrainingSeed(seed_code=seed_code, vector=vec_norm, raw_traits=traits)


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
# 3. Training Plan Generation from TrainingSeed (Demo Logic)
# ============================================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def build_training_plan(seed: TrainingSeed) -> pd.DataFrame:
    """
    Generate a training plan with phases and rough hyperparam styles:
      - dataset size scale
      - model size
      - epochs
      - batch size
      - learning rate scale
      - augmentation level
      - regularization level
      - experiments count
    based on TrainingSeed traits.
    """
    traits = seed.raw_traits

    # 0–10 -> 0–1
    s = lambda name: traits[name] / 10.0

    data_rich = s("Data Richness Preference")
    acc = s("Accuracy Priority")
    speed = s("Training Speed Priority")
    reg = s("Regularization Strength")
    aug = s("Augmentation Intensity")
    exp = s("Experimentation Breadth")
    edge = s("On-Device / Edge Focus")
    interp = s("Interpretability Priority")

    # Base ranges (interpretation)
    # dataset: small (0.2) to huge (1.5)
    # model size: small (0.3) to huge (1.5)
    # epochs: 5–200
    # batch size: 16–2048
    # lr scale: 0.2–2.0
    # aug/reg: 0–100
    # experiments: 1–100

    def dataset_scale(multiplier: float = 1.0) -> float:
        base = 0.2 + 1.3 * data_rich
        return round(base * multiplier, 2)

    def model_scale(multiplier: float = 1.0) -> float:
        # high accuracy → bigger; high edge → smaller
        base = 0.3 + 1.2 * acc
        base *= (0.7 + 0.3 * (1.0 - edge))
        return round(base * multiplier, 2)

    def epoch_count(base: int, scale_factor: float = 1.0) -> int:
        # speed trades off with acc and reg
        base_epochs = base + int(80 * acc + 40 * reg - 60 * speed)
        base_epochs = clamp(base_epochs, 5, 200)
        return int(base_epochs * scale_factor)

    def batch_size() -> int:
        # high speed & edge focus: larger batch (if GPU), otherwise moderate
        base_bs = 32 + int(512 * speed + 256 * edge)
        return int(clamp(base_bs, 16, 2048))

    def lr_scale() -> float:
        # more reg/aug → can tolerate higher LR; high accuracy → moderate LR
        lr = 0.2 + 1.0 * speed + 0.5 * aug + 0.3 * reg - 0.5 * acc
        return round(clamp(lr, 0.2, 2.0), 2)

    def aug_level(multiplier: float = 1.0) -> int:
        # interpretability often prefers simpler schemes
        val = 100 * aug * multiplier * (0.7 + 0.3 * (1.0 - interp))
        return int(clamp(val, 0, 100))

    def reg_level(multiplier: float = 1.0) -> int:
        val = 100 * reg * multiplier
        return int(clamp(val, 0, 100))

    def exp_count(multiplier: float = 1.0) -> int:
        base_exp = 1 + int(90 * exp * multiplier)
        return int(clamp(base_exp, 1, 100))

    phases = []

    # Phase 1: Base model / backbone
    phases.append(
        {
            "Phase": "Base Pretraining / Backbone",
            "Dataset Scale (×)": dataset_scale(1.0),
            "Model Size (×)": model_scale(1.0),
            "Epochs": epoch_count(20, 1.0),
            "Batch Size": batch_size(),
            "LR Scale": lr_scale(),
            "Augmentation (0–100)": aug_level(0.7),
            "Regularization (0–100)": reg_level(0.6),
            "Experiments (runs)": exp_count(0.4),
            "Notes": "Core representation learning; large-ish dataset if data-rich.",
        }
    )

    # Phase 2: Domain fine-tuning
    phases.append(
        {
            "Phase": "Domain Fine-Tuning",
            "Dataset Scale (×)": dataset_scale(0.4),
            "Model Size (×)": model_scale(1.0),
            "Epochs": epoch_count(10, 0.8),
            "Batch Size": batch_size(),
            "LR Scale": round(lr_scale() * 0.6, 2),
            "Augmentation (0–100)": aug_level(1.0),
            "Regularization (0–100)": reg_level(0.8),
            "Experiments (runs)": exp_count(0.6),
            "Notes": "Task-specific data, heavier aug/reg when accuracy is high priority.",
        }
    )

    # Phase 3: Hyperparam sweep / experimentation
    phases.append(
        {
            "Phase": "Hyperparam Sweep",
            "Dataset Scale (×)": dataset_scale(0.3),
            "Model Size (×)": model_scale(1.0),
            "Epochs": epoch_count(5, 0.7),
            "Batch Size": batch_size(),
            "LR Scale": lr_scale(),
            "Augmentation (0–100)": aug_level(0.8),
            "Regularization (0–100)": reg_level(0.7),
            "Experiments (runs)": exp_count(1.0),
            "Notes": "Multiple configs; experimentation breadth controls number of runs.",
        }
    )

    # Phase 4: Distillation / edge deployment (if edge high)
    if traits["On-Device / Edge Focus"] > 2.0:
        phases.append(
            {
                "Phase": "Distillation / Edge Model",
                "Dataset Scale (×)": dataset_scale(0.2),
                "Model Size (×)": round(model_scale(0.5), 2),
                "Epochs": epoch_count(8, 0.7),
                "Batch Size": batch_size(),
                "LR Scale": round(lr_scale() * 0.8, 2),
                "Augmentation (0–100)": aug_level(0.6),
                "Regularization (0–100)": reg_level(0.9),
                "Experiments (runs)": exp_count(0.5),
                "Notes": "Compress to smaller model; more reg; suitable for on-device.",
            }
        )

    # Phase 5: Interpretability / monitoring (if high priority)
    if traits["Interpretability Priority"] > 4.0:
        phases.append(
            {
                "Phase": "Interpretability & Monitoring",
                "Dataset Scale (×)": dataset_scale(0.2),
                "Model Size (×)": model_scale(0.8),
                "Epochs": epoch_count(5, 0.5),
                "Batch Size": batch_size(),
                "LR Scale": round(lr_scale() * 0.5, 2),
                "Augmentation (0–100)": aug_level(0.4),
                "Regularization (0–100)": reg_level(0.5),
                "Experiments (runs)": exp_count(0.3),
                "Notes": "Calibrate, log-rich models, simpler variants for explainability.",
            }
        )

    df = pd.DataFrame(phases)
    return df


# ============================================================
# 4. Storage & Bandwidth Estimates
# ============================================================

def estimate_storage_bytes_per_training_profile(num_traits: int, approx_config_params: int = 40) -> int:
    """
    Assume you store:
    - one float per trait
    - plus ~approx_config_params floats for concrete hyperparams, thresholds, etc.
    """
    return (num_traits + approx_config_params) * BYTES_PER_FLOAT


def estimate_storage_bytes_per_training_seed(seed_code: str) -> int:
    return len(seed_code) * BYTES_PER_CHAR


# ============================================================
# 5. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE ML Training Seed Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE ML Training & Seed Compression Demo")

st.write(
    """
This demo shows how an **MSE-style TrainingSeed** can represent an ML team's
**training style & hyperparam tendencies**, and how that saves **storage and bandwidth**.

- You control **training traits** via sliders.
- The app builds a tiny **TrainingSeed** from those traits.
- That seed generates a **multi-phase training plan**.
- Then we estimate **storage/bandwidth savings** for seeds vs full configs.
"""
)

# Sidebar: traits
st.sidebar.header("🤖 Training Traits")

st.sidebar.write("Set your ML training preferences (0 = not at all, 10 = very strong).")

default_traits = {
    "Data Richness Preference": 7.0,
    "Accuracy Priority": 8.0,
    "Training Speed Priority": 4.0,
    "Regularization Strength": 6.0,
    "Augmentation Intensity": 5.0,
    "Experimentation Breadth": 7.0,
    "On-Device / Edge Focus": 3.0,
    "Interpretability Priority": 5.0,
}

trait_values: Dict[str, float] = {}
for trait in TRAINING_TRAITS:
    trait_values[trait] = st.sidebar.slider(trait, 0.0, 10.0, float(default_traits[trait]), 0.5)

show_raw_profile = st.sidebar.checkbox("Show raw training trait profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized training style vector (debug)", value=False)

# Build seed and training plan
training_seed = build_training_seed(trait_values)
plan_df = build_training_plan(training_seed)

# Layout columns
col_left, col_right = st.columns([1.1, 1.7])

with col_left:
    st.subheader("🧬 TrainingSeed & Style Encoding")

    st.markdown(
        f"""
**Step 1 – Traits → TrainingSeed**

- The sliders define your ML **training style**:
  - how much data you prefer to use,
  - whether you prioritize accuracy vs speed,
  - how strong your regularization & augmentation are,
  - whether you push hard on experimentation,
  - whether you care about edge devices and interpretability.

- These traits become a **normalized vector**.
- That vector is encoded into a tiny seed:

> **TrainingSeed:** `{training_seed.seed_code}`

In a full MSE system, this seed could regenerate:

- default hyperparam configs,  
- training curricula,  
- experiment templates,  
- resource allocations (GPU/TPU),  
- on-device vs server model variants.

What you persist/sync is just the **seed**, not a huge config file each time.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw training traits (stay in orchestrator / config UI):**")
        st.json(training_seed.raw_traits)

    if show_vector:
        st.markdown("**Normalized training style vector:**")
        st.write(training_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – From Seed to Training Plan**

The engine uses the TrainingSeed to derive a **multi-phase plan**, including:

- Base pretraining / backbone choices,  
- Domain fine-tuning settings,  
- Hyperparam sweep style,  
- Optional distillation for edge deployment,  
- Optional interpretability/monitoring passes.

This demo uses simple heuristics; a real MSE implementation would encode
much richer morphic rules and auto-derived settings.
"""
    )

with col_right:
    st.subheader("📋 Generated Training Plan (Phases)")

    st.write(
        """
This table shows an **end-to-end training strategy** implied by the current TrainingSeed.
Tweak traits and watch the configuration reshuffle.
"""
    )
    st.dataframe(plan_df, use_container_width=True)

    st.markdown(
        """
Examples:

- Increase **Accuracy Priority** → more epochs, slightly bigger models, more runs.  
- Increase **Training Speed Priority** → fewer epochs, more aggressive LR.  
- Increase **On-Device / Edge Focus** → more emphasis on distillation and smaller models.  
- Increase **Experimentation Breadth** → more hyperparam sweep runs.  
- Increase **Interpretability Priority** → extra monitoring/interpretability phase.
"""
    )

st.markdown("---")

# ============================================================
# 6. Storage & Bandwidth Savings
# ============================================================

st.subheader("💾 Storage & 📡 Bandwidth Savings for Training Configs")

approx_config_params = 40  # rough guess of how many floats/params a config might have
raw_bytes_per_training = estimate_storage_bytes_per_training_profile(len(TRAINING_TRAITS), approx_config_params)
seed_bytes_per_training = estimate_storage_bytes_per_training_seed(training_seed.seed_code)

st.markdown(
    f"""
### Per Training Profile

**Raw training profile storage (traits + config params)**

- {len(TRAINING_TRAITS)} traits + ~{approx_config_params} config params  
- total ~{len(TRAINING_TRAITS) + approx_config_params} floats × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_training} bytes** per profile

**Seed-only training storage**

- `{training_seed.seed_code}` → {len(training_seed.seed_code)} characters × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_training} bytes** per profile

So in this simplified example, the seed is about **{raw_bytes_per_training / max(seed_bytes_per_training,1):.1f}× smaller**  
than storing a full trait+config bundle directly.

In a real MSE system, the seed could also implicitly encode:
- model families,
- curriculum choices,
- resource tiers,
- and experiment graph structure.
"""
)

# Scale for many projects / experiments
scale_profiles = [100, 10_000, 1_000_000]
rows_storage = []
for n_profiles in scale_profiles:
    raw_total = raw_bytes_per_training * n_profiles
    seed_total = seed_bytes_per_training * n_profiles
    savings = 1.0 - (seed_total / raw_total) if raw_total > 0 else 0.0
    rows_storage.append(
        {
            "Training Profiles": f"{n_profiles:,}",
            "Raw Config Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "Storage Saved": f"{savings*100:.1f}%",
        }
    )

st.markdown("### At Scale (Storage Across Many Experiments / Teams)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
Large orgs often have:

- many projects,  
- many variants per project,  
- multiple environments (dev, staging, prod),  
- long-lived config histories.

Encoding much of that into **TrainingSeeds (+ small deltas)** keeps the config surface lean.
"""
)

# Bandwidth section
st.markdown("### Bandwidth for Orchestrator ↔ Workers / Cloud")

st.markdown(
    """
Now imagine sending training configs to:

- distributed workers,  
- remote clusters,  
- AutoML / experiment services.

Instead of pushing full configs each time, you can:

- send a **TrainingSeed**,  
- let workers regenerate the full config locally.

Below is a rough comparison of sending full configs vs seeds when dispatching jobs.
"""
)

jobs_per_day = st.slider("Assumed training jobs dispatched per day", 10, 500_000, 10_000, step=10)
workers_in_fleet = st.slider("Number of workers receiving configs per day", 10, 100_000, 1_000, step=10)

# Simple model: each job sends its config to one worker
raw_payload_per_job = raw_bytes_per_training
seed_payload_per_job = seed_bytes_per_training
raw_per_day = raw_payload_per_job * jobs_per_day
seed_per_day = seed_payload_per_job * jobs_per_day
savings_per_day = 1.0 - (seed_per_day / raw_per_day) if raw_per_day > 0 else 0.0

rows_bandwidth = [
    {
        "Scenario": "Per job dispatched",
        "Raw Config Payload": human_readable_bytes(raw_payload_per_job),
        "Seed Payload": human_readable_bytes(seed_payload_per_job),
        "Bandwidth Saved": f"{(1 - seed_payload_per_job / raw_payload_per_job)*100:.1f}%" if raw_payload_per_job > 0 else "0%",
    },
    {
        "Scenario": "Per day (all jobs)",
        "Raw Config Payload": human_readable_bytes(int(raw_per_day)),
        "Seed Payload": human_readable_bytes(int(seed_per_day)),
        "Bandwidth Saved": f"{savings_per_day*100:.1f}%",
    },
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
In practice, **seed-based ML training** lets you:

- reuse structured training recipes across teams and models,  
- version and diff seeds instead of giant YAMLs,  
- sync high-level behavior (e.g., "aggressive experimentation, edge-focused")
  across fleets with a few bytes.

This is the ML-training version of your MSE idea:

> **Rich training strategies, tiny deterministic seeds.**
"""
)

import hashlib
from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. QA / Compliance Traits & Storage Model
# ============================================================

QA_TRAITS = [
    "Regulatory Strictness",        # high = more formal controls
    "Risk Aversion",                # high = low tolerance for defects/incidents
    "Automation Level",             # high = heavy automated checks
    "Manual Review Depth",          # high = deep human review
    "Documentation Depth",          # high = detailed evidence & SOP
    "Audit Frequency Preference",   # high = frequent internal audits
    "Sampling Intensity",           # high = large sample sizes / coverage
    "Training & Awareness Emphasis" # high = more training, campaigns
]

BYTES_PER_FLOAT = 4   # e.g., float32 for config weights
BYTES_PER_CHAR = 1    # approx per character


@dataclass
class ComplianceSeed:
    """Tiny, shareable representation of a QA/compliance profile."""
    seed_code: str
    vector: np.ndarray
    raw_traits: Dict[str, float]


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


def build_compliance_seed(traits: Dict[str, float]) -> ComplianceSeed:
    vec = np.array([traits[t] for t in QA_TRAITS], dtype=float)
    vec_norm = normalize_vector(vec)
    seed_code = hash_vector_to_code("QA", vec_norm)
    return ComplianceSeed(seed_code=seed_code, vector=vec_norm, raw_traits=traits)


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


def pct_saved(old: int, new: int) -> float:
    if old <= 0:
        return 0.0
    return 100.0 * (1.0 - (new / old))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


# ============================================================
# 3. Plan Generation from ComplianceSeed (Demo Logic)
# ============================================================

def build_qa_compliance_plan(seed: ComplianceSeed) -> pd.DataFrame:
    """
    Generate a multi-step QA/compliance program plan:
      - phase name
      - automation vs manual
      - sampling coverage
      - audit frequency
      - documentation expectations
      - training cadence
    based on ComplianceSeed traits.
    """
    traits = seed.raw_traits

    s = lambda name: traits[name] / 10.0  # 0–10 -> 0–1

    reg = s("Regulatory Strictness")
    risk = s("Risk Aversion")
    auto = s("Automation Level")
    manual = s("Manual Review Depth")
    doc = s("Documentation Depth")
    audit = s("Audit Frequency Preference")
    sample = s("Sampling Intensity")
    train = s("Training & Awareness Emphasis")

    phases = []

    # Phase 1: Baseline QA & Controls
    automation_pct = clamp(20 + 60 * auto, 0, 100)
    manual_pct = clamp(20 + 60 * manual, 0, 100)
    coverage = clamp(50 + 40 * sample + 10 * risk, 0, 100)
    doc_level = clamp(40 + 50 * doc + 10 * reg, 0, 100)
    audit_freq = clamp(10 + 60 * audit + 20 * reg, 0, 100)
    training_cadence = clamp(20 + 50 * train, 0, 100)

    phases.append(
        {
            "Phase": "Baseline QA & Controls",
            "Automation Intensity (0–100)": round(automation_pct, 1),
            "Manual Review Intensity (0–100)": round(manual_pct, 1),
            "Sampling / Coverage (0–100)": round(coverage, 1),
            "Documentation Rigor (0–100)": round(doc_level, 1),
            "Audit Frequency (0–100)": round(audit_freq, 1),
            "Training Cadence (0–100)": round(training_cadence, 1),
            "Notes": "Establish core QA checks, baseline sampling, and documentation standards."
        }
    )

    # Phase 2: High-Risk / Regulated Areas
    high_risk_boost = 0.2 + 0.8 * max(reg, risk)
    automation_pct_hr = clamp(automation_pct + 10 * auto, 0, 100)
    manual_pct_hr = clamp(manual_pct + 20 * manual + 10 * risk, 0, 100)
    coverage_hr = clamp(coverage + 20 * high_risk_boost, 0, 100)
    doc_level_hr = clamp(doc_level + 20 * reg, 0, 100)
    audit_freq_hr = clamp(audit_freq + 20 * reg + 15 * risk, 0, 100)
    training_cadence_hr = clamp(training_cadence + 20 * train, 0, 100)

    phases.append(
        {
            "Phase": "High-Risk / Regulated Areas",
            "Automation Intensity (0–100)": round(automation_pct_hr, 1),
            "Manual Review Intensity (0–100)": round(manual_pct_hr, 1),
            "Sampling / Coverage (0–100)": round(coverage_hr, 1),
            "Documentation Rigor (0–100)": round(doc_level_hr, 1),
            "Audit Frequency (0–100)": round(audit_freq_hr, 1),
            "Training Cadence (0–100)": round(training_cadence_hr, 1),
            "Notes": "Stricter controls, more evidence, and more frequent checks for high-risk areas."
        }
    )

    # Phase 3: Automation Expansion & Tooling
    # Here automation is emphasized, manual may be optimized.
    automation_pct_auto = clamp(automation_pct + 30 * auto, 0, 100)
    manual_pct_auto = clamp(manual_pct - 20 * auto + 10 * manual, 0, 100)
    coverage_auto = clamp(coverage + 10 * auto, 0, 100)
    doc_level_auto = clamp(doc_level + 10 * doc, 0, 100)
    audit_freq_auto = clamp(audit_freq + 10 * audit, 0, 100)
    training_cadence_auto = clamp(training_cadence + 10 * train, 0, 100)

    phases.append(
        {
            "Phase": "Automation Expansion & Tooling",
            "Automation Intensity (0–100)": round(automation_pct_auto, 1),
            "Manual Review Intensity (0–100)": round(manual_pct_auto, 1),
            "Sampling / Coverage (0–100)": round(coverage_auto, 1),
            "Documentation Rigor (0–100)": round(doc_level_auto, 1),
            "Audit Frequency (0–100)": round(audit_freq_auto, 1),
            "Training Cadence (0–100)": round(training_cadence_auto, 1),
            "Notes": "Scale automated QA, refine human review, and improve tool coverage."
        }
    )

    # Phase 4: Continuous Monitoring & Auditing
    automation_pct_mon = clamp(automation_pct_auto, 0, 100)
    manual_pct_mon = clamp(manual_pct_auto, 0, 100)
    coverage_mon = clamp(coverage_hr, 0, 100)
    doc_level_mon = clamp(doc_level_hr + 10 * doc, 0, 100)
    audit_freq_mon = clamp(audit_freq_hr + 10 * audit, 0, 100)
    training_cadence_mon = clamp(training_cadence_hr, 0, 100)

    phases.append(
        {
            "Phase": "Continuous Monitoring & Auditing",
            "Automation Intensity (0–100)": round(automation_pct_mon, 1),
            "Manual Review Intensity (0–100)": round(manual_pct_mon, 1),
            "Sampling / Coverage (0–100)": round(coverage_mon, 1),
            "Documentation Rigor (0–100)": round(doc_level_mon, 1),
            "Audit Frequency (0–100)": round(audit_freq_mon, 1),
            "Training Cadence (0–100)": round(training_cadence_mon, 1),
            "Notes": "Implement continuous monitoring, regular internal audits, and ongoing training."
        }
    )

    # Phase 5: Culture, Training, & Improvement
    if traits["Training & Awareness Emphasis"] > 3.0:
        automation_pct_culture = clamp(automation_pct_mon, 0, 100)
        manual_pct_culture = clamp(manual_pct_mon, 0, 100)
        coverage_culture = clamp(coverage_mon, 0, 100)
        doc_level_culture = clamp(doc_level_mon, 0, 100)
        audit_freq_culture = clamp(audit_freq_mon, 0, 100)
        training_cadence_culture = clamp(training_cadence_mon + 20 * train, 0, 100)

        phases.append(
            {
                "Phase": "Culture & Continuous Improvement",
                "Automation Intensity (0–100)": round(automation_pct_culture, 1),
                "Manual Review Intensity (0–100)": round(manual_pct_culture, 1),
                "Sampling / Coverage (0–100)": round(coverage_culture, 1),
                "Documentation Rigor (0–100)": round(doc_level_culture, 1),
                "Audit Frequency (0–100)": round(audit_freq_culture, 1),
                "Training Cadence (0–100)": round(training_cadence_culture, 1),
                "Notes": "Embed QA/compliance into culture: recurring training, retrospectives, and improvement cycles."
            }
        )

    df = pd.DataFrame(phases)
    return df


# ============================================================
# 4. Storage & Bandwidth Estimates
# ============================================================

def estimate_storage_bytes_per_qa_profile(num_traits: int, approx_config_params: int = 40) -> int:
    """
    Assume you store:
    - one float per trait
    - plus ~approx_config_params floats for thresholds, matrices, playbooks, etc.
    """
    return (num_traits + approx_config_params) * BYTES_PER_FLOAT


def estimate_storage_bytes_per_seed(seed_code: str) -> int:
    return len(seed_code) * BYTES_PER_CHAR


# ============================================================
# 5. Streamlit UI
# ============================================================

st.set_page_config(
    page_title="MSE QA / Compliance Seed Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE QA / Compliance & Seed Compression Demo")

st.write(
    """
This demo shows how an **MSE-style ComplianceSeed** can represent a team's
**QA/compliance posture**, and how that saves **storage and bandwidth**.

- You control **QA/compliance traits** via sliders.
- The app builds a tiny **ComplianceSeed** from those traits.
- That seed generates a **multi-phase QA/compliance program**.
- Then we estimate **storage/bandwidth savings** for seeds vs full policy/config packages.
"""
)

# Sidebar: traits
st.sidebar.header("✅ QA / Compliance Traits")

st.sidebar.write("Set your QA/compliance tendencies (0 = low emphasis, 10 = very strong).")

default_traits = {
    "Regulatory Strictness": 7.0,
    "Risk Aversion": 8.0,
    "Automation Level": 6.0,
    "Manual Review Depth": 5.0,
    "Documentation Depth": 7.0,
    "Audit Frequency Preference": 6.0,
    "Sampling Intensity": 5.0,
    "Training & Awareness Emphasis": 6.0,
}

trait_values: Dict[str, float] = {}
for trait in QA_TRAITS:
    trait_values[trait] = st.sidebar.slider(trait, 0.0, 10.0, float(default_traits[trait]), 0.5)

show_raw_profile = st.sidebar.checkbox("Show raw QA/compliance profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized QA/compliance vector (debug)", value=False)

# Build seed and plan
compliance_seed = build_compliance_seed(trait_values)
plan_df = build_qa_compliance_plan(compliance_seed)

# Layout columns
col_left, col_right = st.columns([1.1, 1.7])

with col_left:
    st.subheader("🧬 ComplianceSeed & Profile Encoding")

    st.markdown(
        f"""
**Step 1 – Traits → ComplianceSeed**

Your sliders define your **QA/compliance posture**:

- how strict your regulatory stance is,  
- how much risk you tolerate,  
- how automated vs manual you are,  
- how deep documentation and audits should go,  
- how often you invest in training and awareness.

These traits become a **normalized vector** and are encoded into a small seed:

> **ComplianceSeed:** `{compliance_seed.seed_code}`

In a full MSE system, this seed could regenerate:

- control catalogs & test templates,  
- risk-based sampling schemes,  
- audit calendars & checklists,  
- training cadences and playbooks.

What you persist/sync is just the **seed**, not huge XML/YAML/Word policy bundles.
"""
    )

    if show_raw_profile:
        st.markdown("**Local raw QA/compliance traits (stay in the governance tool):**")
        st.json(compliance_seed.raw_traits)

    if show_vector:
        st.markdown("**Normalized QA/compliance style vector:**")
        st.write(compliance_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – From Seed to QA / Compliance Plan**

The engine uses the ComplianceSeed to derive a **multi-phase program**:

- Baseline QA & controls,  
- High-risk / regulated area controls,  
- Automation expansion,  
- Continuous monitoring & audits,  
- (Optionally) culture & continuous improvement.

This demo uses simple heuristics; an actual MSE implementation would encode
richer morphic rules, mapping seeds to detailed control sets and workflows.
"""
    )

with col_right:
    st.subheader("📋 Generated QA / Compliance Program (Phases)")

    st.write(
        """
This table shows an **end-to-end QA/compliance strategy** implied by the current ComplianceSeed.
Tweak traits and see intensity, coverage, and cadence change.
"""
    )
    st.dataframe(plan_df, use_container_width=True)

    st.markdown(
        """
Examples:

- Increase **Regulatory Strictness** → more documentation, more audits.  
- Increase **Risk Aversion** → higher coverage & stricter reviews.  
- Increase **Automation Level** → stronger automation phase.  
- Increase **Training & Awareness Emphasis** → more culture-focused phase.
"""
    )

st.markdown("---")

# ============================================================
# 6. Storage & Bandwidth Savings
# ============================================================

st.subheader("💾 Storage & 📡 Bandwidth Savings for QA / Compliance Profiles")

approx_config_params = 40  # rough guess of config thresholds, matrices, etc.
raw_bytes_per_profile = estimate_storage_bytes_per_qa_profile(len(QA_TRAITS), approx_config_params)
seed_bytes_per_profile = estimate_storage_bytes_per_seed(compliance_seed.seed_code)

st.markdown(
    f"""
### Per QA / Compliance Profile

**Raw QA/compliance config storage (traits + detailed params)**

- {len(QA_TRAITS)} traits + ~{approx_config_params} config params  
- total ~{len(QA_TRAITS) + approx_config_params} floats × {BYTES_PER_FLOAT} bytes/float  
- ≈ **{raw_bytes_per_profile} bytes** per profile

**Seed-only QA/compliance storage**

- `{compliance_seed.seed_code}` → {len(compliance_seed.seed_code)} chars × {BYTES_PER_CHAR} byte/char  
- ≈ **{seed_bytes_per_profile} bytes** per profile

So in this simplified example, the seed is about **{raw_bytes_per_profile / max(seed_bytes_per_profile,1):.1f}× smaller**  
than storing the full trait + config bundle directly.
"""
)

# Scale across many teams/regions
scale_profiles = [10, 1_000, 100_000, 1_000_000]
rows_storage = []
for n_profiles in scale_profiles:
    raw_total = raw_bytes_per_profile * n_profiles
    seed_total = seed_bytes_per_profile * n_profiles
    savings_pct = pct_saved(raw_total, seed_total)
    rows_storage.append(
        {
            "QA / Compliance Profiles": f"{n_profiles:,}",
            "Raw Config Storage": human_readable_bytes(raw_total),
            "Seed-Only Storage": human_readable_bytes(seed_total),
            "% Storage Saved": f"{savings_pct:.1f}%",
        }
    )

st.markdown("### At Scale (Storage Across Many Teams / Business Units)")
st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
Large organizations often have:

- many teams or regions,  
- multiple product lines,  
- different regulatory regimes (GDPR, HIPAA, SOX, PCI, etc.),  
- long-lived policy/config histories.

Encoding much of that into **ComplianceSeeds (+ small deltas)** keeps the governance surface lean while preserving structure.
"""
)

# Bandwidth section
st.subheader("📡 Bandwidth for Governance Tools & Audit Systems")

st.markdown(
    """
Now imagine syncing QA/compliance configs between:

- central governance tool ↔ local QA tools,  
- QA tools ↔ CI/CD systems,  
- policy engines ↔ audit/reporting platforms.

Instead of shipping full policy/config blobs each time, you can:

- send a **ComplianceSeed**,  
- let each tool regenerate the full config and controls locally.
"""
)

syncs_per_day = st.slider("Assumed QA/compliance syncs per profile per day", 1, 200, 20)
profiles_in_system = st.slider("Number of QA/compliance profiles (teams / regions)", 10, 50_000, 5_000, step=10)

raw_payload_per_sync = raw_bytes_per_profile * profiles_in_system
seed_payload_per_sync = seed_bytes_per_profile * profiles_in_system
raw_per_day = raw_payload_per_sync * syncs_per_day
seed_per_day = seed_payload_per_sync * syncs_per_day
savings_per_day_pct = pct_saved(raw_per_day, seed_per_day)

rows_bandwidth = [
    {
        "Scenario": "Per sync (all profiles)",
        "Raw Config Payload": human_readable_bytes(raw_payload_per_sync),
        "Seed Payload": human_readable_bytes(seed_payload_per_sync),
        "% Bandwidth Saved": f"{pct_saved(raw_payload_per_sync, seed_payload_per_sync):.1f}%",
    },
    {
        "Scenario": "Per day (all syncs)",
        "Raw Config Payload": human_readable_bytes(int(raw_per_day)),
        "Seed Payload": human_readable_bytes(int(seed_per_day)),
        "% Bandwidth Saved": f"{savings_per_day_pct:.1f}%",
    },
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
With thousands of profiles and frequent updates:

- **Seed-based QA/compliance** shrinks the config footprint,  
- makes multi-tool integration cheaper,  
- and still lets you encode very rich behavior and control structure.

This is the **QA/compliance** angle of your MSE story:

> **Complex governance, tiny deterministic seeds, real % savings.**
"""
)

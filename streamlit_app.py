import hashlib
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. Catalog Attributes & Storage Model
# ============================================================

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Sports",
    "Books",
    "Toys",
    "Beauty",
    "Grocery",
]

BRANDS = [
    "Acme",
    "HyperNova",
    "Northwind",
    "Orion",
    "NovaTech",
    "Skyline",
    "Lumos",
    "Cascade",
]

# Rough storage assumptions
BYTES_PER_CHAR = 1            # approx per character
UUID_LENGTH = 36              # typical v4 UUID string length: 8-4-4-4-12
CLASSIC_SKU_LENGTH = 24       # e.g., "ELEC-ACM-2025-000123" (illustrative)


@dataclass
class CatalogSeed:
    """Tiny, structured representation of a catalog item family."""
    seed_code: str                # e.g. "CAT-3F9A2C"
    vector: np.ndarray            # normalized attribute vector (local only)
    raw_attributes: Dict[str, str]  # human-readable attributes


# ============================================================
# 2. Helper Functions
# ============================================================

def encode_category(cat: str) -> int:
    return CATEGORIES.index(cat)


def encode_brand(brand: str) -> int:
    return BRANDS.index(brand)


def normalize_vector(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def hash_vector_to_seed(prefix: str, v: np.ndarray) -> str:
    """
    Turn a numeric vector into a short deterministic seed code.
    In a full MSE, this would be a morphic seed; here it's a simple hash.
    """
    q = np.round(v * 100).astype(int)
    raw = ",".join(map(str, q.tolist())).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:6].upper()
    return f"{prefix}-{digest}"


def build_catalog_seed(
    category: str,
    brand: str,
    price_tier: int,
    seasonality: int,
    year: int,
) -> CatalogSeed:
    """
    Build a CatalogSeed from a few key attributes.
    Vector is numeric; raw_attributes is human-readable.
    """
    cat_idx = encode_category(category)
    brand_idx = encode_brand(brand)

    # Simple numeric vector: [cat_idx, brand_idx, price_tier, seasonality, year_mod]
    year_mod = year % 100  # last two digits
    v = np.array(
        [
            cat_idx,
            brand_idx,
            float(price_tier),
            float(seasonality),
            float(year_mod),
        ],
        dtype=float,
    )
    v_norm = normalize_vector(v)
    seed_code = hash_vector_to_seed("CAT", v_norm)
    attrs = {
        "category": category,
        "brand": brand,
        "price_tier": str(price_tier),
        "seasonality": str(seasonality),
        "year": str(year),
    }
    return CatalogSeed(seed_code=seed_code, vector=v_norm, raw_attributes=attrs)


def build_catalog_id(seed: CatalogSeed, variant_index: int) -> str:
    """
    Build a compact CatalogID from:
    - category abbrev
    - brand abbrev
    - year suffix
    - seed hash suffix
    - variant index
    Example: ELE-ACM-25-C3F9-0012
    """
    cat = seed.raw_attributes["category"]
    brand = seed.raw_attributes["brand"]
    year = int(seed.raw_attributes["year"])
    year_suffix = str(year % 100).zfill(2)

    cat_abbrev = cat.replace("&", "").replace(" ", "")[:3].upper()
    brand_abbrev = brand[:3].upper()

    # Take last 4 chars of seed code digest for brevity
    digest_part = seed.seed_code.split("-")[-1][-4:]
    variant_str = str(variant_index).zfill(4)

    return f"{cat_abbrev}-{brand_abbrev}-{year_suffix}-{digest_part}-{variant_str}"


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


# ============================================================
# 3. Streamlit UI Setup
# ============================================================

st.set_page_config(
    page_title="MSE Catalog ID / UUID Seed Demo",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 MSE Catalog ID & UUID-Style Seed Demo")

st.write(
    """
This demo shows how an **MSE-style CatalogSeed** can replace or augment
classic **UUIDs / catalog IDs**, while saving **storage and bandwidth**.

- You define **catalog attributes** (category, brand, price tier, etc.).
- The app computes a compact **CatalogSeed** and uses it to create **CatalogIDs**.
- IDs are structured and deterministic, encoding product family + variant.
- We then compare **storage & bandwidth**, including **% saved**, vs:
  - classic random UUIDs, and
  - longer SKU-style IDs.
"""
)

# ============================================================
# 4. Sidebar: Catalog Attributes
# ============================================================

st.sidebar.header("📦 Catalog Item Family")

category = st.sidebar.selectbox("Category", CATEGORIES, index=0)
brand = st.sidebar.selectbox("Brand", BRANDS, index=0)

price_tier = st.sidebar.slider(
    "Price Tier (1 = budget, 5 = premium)",
    min_value=1,
    max_value=5,
    value=3,
)
seasonality = st.sidebar.slider(
    "Seasonality (0 = evergreen, 10 = highly seasonal)",
    min_value=0,
    max_value=10,
    value=4,
)
year = st.sidebar.slider("Release Year", min_value=2015, max_value=2035, value=2025, step=1)

num_variants = st.sidebar.slider("Number of variants to generate", 1, 50, 10, 1)

show_raw_attrs = st.sidebar.checkbox("Show raw attribute profile (local only)", value=True)
show_vector = st.sidebar.checkbox("Show normalized attribute vector (debug)", value=False)

# ============================================================
# 5. Build Seed and Example Catalog IDs
# ============================================================

catalog_seed = build_catalog_seed(category, brand, price_tier, seasonality, year)

rows_items: List[Dict[str, str]] = []
for idx in range(1, num_variants + 1):
    cat_id = build_catalog_id(catalog_seed, variant_index=idx)
    rows_items.append(
        {
            "Variant #": idx,
            "CatalogID (Seed-based)": cat_id,
        }
    )

items_df = pd.DataFrame(rows_items)

# ============================================================
# 6. Layout: Seed Explanation & Catalog IDs
# ============================================================

col_left, col_right = st.columns([1.1, 1.7])

with col_left:
    st.subheader("🧬 CatalogSeed & Structured ID Family")

    st.markdown(
        f"""
**Step 1 – Attributes → CatalogSeed**

You picked:

- **Category:** `{category}`  
- **Brand:** `{brand}`  
- **Price Tier:** `{price_tier}`  
- **Seasonality:** `{seasonality}`  
- **Year:** `{year}`  

These attributes are encoded as numeric features, normalized, and turned into a short **seed**:

> **CatalogSeed:** `{catalog_seed.seed_code}`

In a full MSE system, that seed could regenerate:

- product family metadata,  
- pricing bands,  
- regional availability,  
- recommendation / personalization behavior.

But what you actually store/transmit is just the **seed** (or short IDs built from it).
"""
    )

    if show_raw_attrs:
        st.markdown("**Local raw attributes (editor / back-office only):**")
        st.json(catalog_seed.raw_attributes)

    if show_vector:
        st.markdown("**Normalized attribute vector:**")
        st.write(catalog_seed.vector)

    st.markdown("---")

    st.markdown(
        """
**Step 2 – Seed → CatalogID Series**

From the CatalogSeed, we generate **variant IDs** that encode:

- category abbreviation,  
- brand abbreviation,  
- year suffix,  
- a seed hash fragment,  
- variant index.

This gives you deterministic, structured IDs that behave like UUIDs, but can be:

- shorter,  
- semantically meaningful,  
- consistent per product family.
"""
    )

with col_right:
    st.subheader("📋 Generated Catalog IDs for This Product Family")

    st.write(
        f"""
Below are **{num_variants}** example CatalogIDs derived from this **one** CatalogSeed.
The IDs share a family signature (same category, brand, year + seed hash).
"""
    )
    st.dataframe(items_df, use_container_width=True)

    st.markdown(
        """
You might:

- Use the **CatalogSeed** internally to regenerate full metadata.  
- Use the **CatalogID** as a public/DB key.  
- Optionally still keep a random UUID for strict global uniqueness, while
  the seed gives you a semantic “handle” on the product family.
"""
    )

st.markdown("---")

# ============================================================
# 7. Storage Savings (with %)
# ============================================================

st.subheader("💾 Storage Savings for Catalog IDs")

# Per-ID comparison
seed_based_id_example = items_df["CatalogID (Seed-based)"].iloc[0]
seed_id_length = len(seed_based_id_example)
seed_code_length = len(catalog_seed.seed_code)

uuid_bytes = UUID_LENGTH * BYTES_PER_CHAR
sku_bytes = CLASSIC_SKU_LENGTH * BYTES_PER_CHAR
seed_id_bytes = seed_id_length * BYTES_PER_CHAR
seed_code_bytes = seed_code_length * BYTES_PER_CHAR

uuid_vs_seed_id_pct = pct_saved(uuid_bytes, seed_id_bytes)
sku_vs_seed_id_pct = pct_saved(sku_bytes, seed_id_bytes)

st.markdown(
    f"""
### Per ID / Seed

**Classic UUID v4 string**  
- Length: **{UUID_LENGTH}** chars  
- Storage: **{uuid_bytes} bytes** per ID  

**Classic SKU-style ID (example)**  
- Approx length: **{CLASSIC_SKU_LENGTH}** chars  
- Storage: **{sku_bytes} bytes** per ID  

**Seed-based CatalogID (demo)**  
- Example: `{seed_based_id_example}`  
- Length: **{seed_id_length}** chars  
- Storage: **{seed_id_bytes} bytes** per ID  
- **Storage saved vs UUID:** ~**{uuid_vs_seed_id_pct:.1f}%**  
- **Storage saved vs classic SKU:** ~**{sku_vs_seed_id_pct:.1f}%**  

**CatalogSeed** (shared across variants in the same family)  
- `{catalog_seed.seed_code}`  
- Length: **{seed_code_length}** chars  
- Storage: **{seed_code_bytes} bytes** per seed
"""
)

# At catalog scale
st.markdown("### At Catalog Scale (Storage Across Many Items)")

catalog_sizes = [10_000, 1_000_000, 100_000_000]
rows_storage = []

for n_items in catalog_sizes:
    uuid_total = uuid_bytes * n_items
    sku_total = sku_bytes * n_items
    seed_id_total = seed_id_bytes * n_items

    # Assume ~1 seed per 100 items (family concept)
    num_seeds = max(1, n_items // 100)
    seeds_total = seed_code_bytes * num_seeds

    # Total with seed system = IDs + seeds
    total_seed_system = seed_id_total + seeds_total

    uuid_pct_saved = pct_saved(uuid_total, total_seed_system)
    sku_pct_saved = pct_saved(sku_total, total_seed_system)

    rows_storage.append(
        {
            "Catalog Size (items)": f"{n_items:,}",
            "UUID-Only Storage": human_readable_bytes(uuid_total),
            "SKU-Only Storage": human_readable_bytes(sku_total),
            "Seed-Based IDs + Seeds": human_readable_bytes(total_seed_system),
            "% Saved vs UUID": f"{uuid_pct_saved:.1f}%",
            "% Saved vs SKU": f"{sku_pct_saved:.1f}%",
        }
    )

st.dataframe(pd.DataFrame(rows_storage), use_container_width=True)

st.markdown(
    """
**Key idea:**

- UUID-only or SKU-only approaches store a full-length ID for *every* item.  
- Seed-based systems use a **shared CatalogSeed** per product family +  
  **shorter IDs** per variant.  
- That reduces total string storage and gives you semantic grouping “for free”.
"""
)

st.markdown("---")

# ============================================================
# 8. Bandwidth Savings (with %)
# ============================================================

st.subheader("📡 Bandwidth Savings for Sync / Export")

st.markdown(
    """
Consider syncing catalog data:

- **PIM → e-commerce**,  
- **e-commerce → search index**,  
- **central DB → caches / edge nodes**.

We compare sending:

- a full UUID per item vs  
- a seed-based ID per item + one CatalogSeed per family.
"""
)

sync_items = st.slider("Items in a sync/export batch", 1_000, 5_000_000, 100_000, step=1_000)

uuid_payload = uuid_bytes * sync_items
sku_payload = sku_bytes * sync_items
seed_id_payload = seed_id_bytes * sync_items

# Assume same 1 seed per 100 items
num_seeds_sync = max(1, sync_items // 100)
seeds_payload = seed_code_bytes * num_seeds_sync

total_seed_sync_payload = seed_id_payload + seeds_payload

uuid_sync_pct_saved = pct_saved(uuid_payload, total_seed_sync_payload)
sku_sync_pct_saved = pct_saved(sku_payload, total_seed_sync_payload)

rows_bandwidth = [
    {
        "Metric": "Payload size for this sync batch",
        "Items in Batch": f"{sync_items:,}",
        "UUID Payload": human_readable_bytes(uuid_payload),
        "SKU Payload": human_readable_bytes(sku_payload),
        "Seed-Based IDs + Seeds": human_readable_bytes(total_seed_sync_payload),
        "% Saved vs UUID": f"{uuid_sync_pct_saved:.1f}%",
        "% Saved vs SKU": f"{sku_sync_pct_saved:.1f}%",
    }
]

st.dataframe(pd.DataFrame(rows_bandwidth), use_container_width=True)

st.markdown(
    """
With millions of items and many syncs:

- **Seed-based IDs** shrink the per-item identifier.  
- **CatalogSeeds** let you share structure once, not per-row.  
- Combined, you get **real % savings** on both storage and bandwidth,
  plus deterministic, semantic IDs mapped back to rich MSE-generated metadata.

This is the catalog / UUID angle of the MSE story:

> **Huge catalogs, small IDs, shared seeds, real % savings.**
"""
)

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Try to import Streamlit; if not installed, CLI mode still works.
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


# ============================================================
# 1. Core data structures
# ============================================================

@dataclass
class MorphProgram:
    family_id: str
    series_length: int
    a: float
    b: float
    smooth_strength: float
    nonlin_strength: float


@dataclass
class TileSeed:
    mode: int                 # 0 = pure MSE, 1 = MSE+residual (not used yet), 2 = raw tokens
    length: int
    norm_min: float
    norm_max: float
    tokens: List[int]         # for now we store explicit tokens; can later compress
    morph_program: MorphProgram
    residuals: Optional[List[float]] = None  # placeholder for mode 1


# ============================================================
# 2. Tokenization / normalization (1..100 tokens)
# ============================================================

def normalize_to_tokens(values: List[float], num_tokens: int = 100) -> Tuple[List[int], Tuple[float, float]]:
    """
    Map arbitrary numeric values to integer tokens in [1..num_tokens].
    Returns (tokens, (min_val, max_val)).
    """
    if len(values) == 0:
        raise ValueError("Array is empty")

    min_val = min(values)
    max_val = max(values)

    if max_val == min_val:
        tokens = [num_tokens // 2] * len(values)
        return tokens, (min_val, max_val)

    span = max_val - min_val
    tokens: List[int] = []
    for x in values:
        # Normalize to [0,1], then to [1..num_tokens]
        norm = (x - min_val) / span
        t = 1 + int(norm * (num_tokens - 1))
        # Safety clamp
        t = max(1, min(num_tokens, t))
        tokens.append(t)
    return tokens, (min_val, max_val)


def tokens_to_base(tokens: List[int], norm_params: Tuple[float, float], num_tokens: int = 100) -> List[float]:
    """
    Convert tokens back to a base numeric approximation using (min, max).
    """
    min_val, max_val = norm_params
    if max_val == min_val:
        return [min_val] * len(tokens)

    span = max_val - min_val
    base: List[float] = []
    for t in tokens:
        # Interpret token t as representing the center of its bin
        frac = (t - 0.5) / num_tokens  # in (0..1)
        x = min_val + frac * span
        base.append(x)
    return base


# ============================================================
# 3. Morph family: terrain_1d_v1
#    (simple: linear + smoothing + token-based nonlinearity)
# ============================================================

def linear_step(x: List[float], a: float, b: float) -> List[float]:
    return [a * xi + b for xi in x]


def smooth_step(x: List[float], strength: float) -> List[float]:
    """
    strength in [0,1]. 0 = no smoothing, 1 = full smoothing.
    Core smoothing: y[i] = (x[i-1] + 2*x[i] + x[i+1]) / 4
    Then blend: out[i] = (1-strength)*x[i] + strength*y[i]
    """
    if strength <= 0.0:
        return x[:]  # no-op

    n = len(x)
    if n == 1:
        return x[:]

    y = [0.0] * n
    for i in range(n):
        left = x[i - 1] if i > 0 else x[i]
        right = x[i + 1] if i < n - 1 else x[i]
        center = x[i]
        sm = (left + 2 * center + right) / 4.0
        y[i] = sm

    out = [(1.0 - strength) * x[i] + strength * y[i] for i in range(n)]
    return out


def nonlin_step(x: List[float], tokens: List[int], strength: float) -> List[float]:
    """
    Simple token-dependent nonlinearity.
    - High tokens (>70) bump values up slightly.
    - Low tokens (<30) bump values down slightly.
    - Mid tokens mostly unchanged.
    strength in [0,1] controls magnitude.
    """
    if strength <= 0.0:
        return x[:]

    n = len(x)
    out = [0.0] * n
    for i in range(n):
        t = tokens[i]
        base = x[i]

        if t > 70:
            # bump up, scaled by how high the token is
            delta = (t - 70) / 30.0  # in (0..1)
            out[i] = base + strength * delta * 0.5  # 0.5 is arbitrary scale
        elif t < 30:
            # bump down
            delta = (30 - t) / 29.0  # in (0..1)
            out[i] = base - strength * delta * 0.5
        else:
            out[i] = base
    return out


def run_morph_program(tokens: List[int],
                      norm_params: Tuple[float, float],
                      program: MorphProgram) -> List[float]:
    """
    Given tokens, normalization params, and a morph program, generate the numeric array.
    """
    # Start from base numeric approximation of tokens
    x = tokens_to_base(tokens, norm_params)

    for _ in range(program.series_length):
        # linear
        x = linear_step(x, program.a, program.b)
        # smoothing
        x = smooth_step(x, program.smooth_strength)
        # non-linear
        x = nonlin_step(x, tokens, program.nonlin_strength)

    return x


# ============================================================
# 4. Error metric
# ============================================================

def mse(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Length mismatch for MSE")
    if not a:
        return 0.0
    s = 0.0
    for x, y in zip(a, b):
        d = x - y
        s += d * d
    return s / len(a)


# ============================================================
# 5. Seed searcher (single tile, bounded grid search)
# ============================================================

@dataclass
class SeedSearchResult:
    seed: TileSeed
    reconstructed: List[float]
    error: float


def search_best_seed_for_tile(values: List[float]) -> SeedSearchResult:
    """
    Very simple, bounded grid search for a best-fit MorphProgram seed
    for a single tile. This is the prototype version, not the final
    production-level searcher.
    """

    # 1. Normalize to tokens
    tokens, (min_val, max_val) = normalize_to_tokens(values)

    length = len(values)

    # 2. Define search grid.
    series_lengths   = [1, 2, 3]
    a_values         = [1.0]                # keep linear step simple for now
    b_values         = [0.0, -0.5, 0.5]     # small offset tweaks
    smooth_strengths = [0.0, 0.3, 0.6]
    nonlin_strengths = [0.0, 0.3, 0.6]

    best_score = float("inf")
    best_program: Optional[MorphProgram] = None
    best_recon: List[float] = []

    # 3. Brute-force over this small parameter grid.
    for T in series_lengths:
        for a in a_values:
            for b in b_values:
                for s_smooth in smooth_strengths:
                    for s_nonlin in nonlin_strengths:
                        program = MorphProgram(
                            family_id="terrain_1d_v1",
                            series_length=T,
                            a=a,
                            b=b,
                            smooth_strength=s_smooth,
                            nonlin_strength=s_nonlin,
                        )
                        recon = run_morph_program(tokens, (min_val, max_val), program)
                        err = mse(values, recon)

                        # Simple complexity penalty (favor fewer iterations & weaker nonlin)
                        complexity = 0.1 * (T - 1) + 0.05 * (s_nonlin > 0.0)
                        score = err + complexity

                        if score < best_score:
                            best_score = score
                            best_program = program
                            best_recon = recon

    # 4. Build TileSeed (mode 0 = pure MSE) with found program.
    if best_program is None:
        # Fallback: no search improvement; just use base tokens with identity morph.
        best_program = MorphProgram(
            family_id="terrain_1d_v1",
            series_length=1,
            a=1.0,
            b=0.0,
            smooth_strength=0.0,
            nonlin_strength=0.0,
        )
        best_recon = run_morph_program(tokens, (min_val, max_val), best_program)
        best_score = mse(values, best_recon)

    tile_seed = TileSeed(
        mode=0,
        length=length,
        norm_min=min_val,
        norm_max=max_val,
        tokens=tokens,
        morph_program=best_program,
        residuals=None,
    )

    return SeedSearchResult(seed=tile_seed, reconstructed=best_recon, error=best_score)


# ============================================================
# 6. Pretty-print helpers
# ============================================================

def summarize_seed(seed: TileSeed) -> str:
    p = seed.morph_program
    return (
        f"TileSeed(mode={seed.mode}, length={seed.length})\n"
        f"  norm_min={seed.norm_min:.4f}, norm_max={seed.norm_max:.4f}\n"
        f"  tokens[0:10]={seed.tokens[:10]}{'...' if len(seed.tokens) > 10 else ''}\n"
        f"  MorphProgram(family_id={p.family_id}, series_length={p.series_length},\n"
        f"               a={p.a}, b={p.b}, smooth_strength={p.smooth_strength},\n"
        f"               nonlin_strength={p.nonlin_strength})"
    )


# ============================================================
# 7. CLI entry point (for quick testing)
# ============================================================

def run_cli_demo():
    print("MSE Seed Searcher Demo (single tile)")
    print("Enter a comma-separated list of numbers, e.g.: 57,1456,34,69")
    raw = input("Array: ").strip()
    if not raw:
        print("No input.")
        return

    try:
        values = [float(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        print("Could not parse numbers.")
        return

    result = search_best_seed_for_tile(values)

    print("\n=== Best Seed Found ===")
    print(summarize_seed(result.seed))
    print(f"\nMSE error: {result.error:.6f}")

    print("\nOriginal vs Reconstructed (first 20 items):")
    for i, (orig, rec) in enumerate(zip(values, result.reconstructed)):
        if i >= 20:
            print("...")
            break
        print(f"{i:3d}: orig={orig:.4f}, recon={rec:.4f}, diff={orig-rec:.4f}")


# ============================================================
# 8. Streamlit app (if Streamlit is installed)
# ============================================================

def run_streamlit_app():
    st.title("MSE Seed Searcher (Prototype)")
    st.write("Given an array of numbers, find a best-fit MSE seed and reconstruct it.")

    default_array = "57, 1456, 34, 69, 120, 980, 43, 88"
    raw = st.text_area("Input array (comma-separated numbers):", value=default_array, height=120)

    if st.button("Search for Seed"):
        try:
            values = [float(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            st.error("Could not parse the input. Make sure it's comma-separated numbers.")
            return

        if not values:
            st.error("Please enter at least one number.")
            return

        result = search_best_seed_for_tile(values)

        st.subheader("Best Seed Found")
        st.code(summarize_seed(result.seed))

        st.subheader("Error")
        st.write(f"Mean Squared Error (MSE): `{result.error:.6f}`")

        # Show original vs reconstructed
        st.subheader("Original vs Reconstructed (first 100 items)")
        n_show = min(100, len(values))
        rows = []
        for i in range(n_show):
            rows.append(
                {
                    "index": i,
                    "original": values[i],
                    "reconstructed": result.reconstructed[i],
                    "diff": values[i] - result.reconstructed[i],
                }
            )

        try:
            import pandas as pd
            df = pd.DataFrame(rows)
            st.dataframe(df)
        except ImportError:
            # Fallback simple text if pandas not available
            st.text("index | original | reconstructed | diff")
            for row in rows:
                st.text(f"{row['index']:3d} | {row['original']:.4f} | {row['reconstructed']:.4f} | {row['diff']:.4f}")


# ============================================================
# 9. Main
# ============================================================

if __name__ == "__main__":
    if HAS_STREAMLIT:
        # Run as a Streamlit app if streamlit is installed and you do:
        #   streamlit run mse_seed_app.py
        run_streamlit_app()
    else:
        # Fallback: plain CLI mode
        run_cli_demo()

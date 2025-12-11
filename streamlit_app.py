import re
import json
import streamlit as st

# -------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------
st.set_page_config(
    page_title="Tiny MSE Compression Demo",
    page_icon="🧬",
    layout="centered",
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <h1 style='font-size:42px; font-weight:700; margin-bottom:0.1em;'>
        Morphic Semantic Engine – Tiny MSE Format
    </h1>
    <h3 style='font-size:20px; font-style:italic; color:#666; margin-top:0;'>
        Enter a seed, prefix, or full code — generate JSON deterministically.
    </h3>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div><div style="font-weight:500; color:#444;">Store complete JSON dictionaries using only compact reversible codes.</div><br><div>The MSE already reduces the need to store information in databases. The standard seed is enough to generate enormous amounts of data in real-time. Using <i>Tiny MSE</i> format, the space used is reduced even further.</div>
        <br>
    </div>
    <hr>
    
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Shared Series Mode
# -------------------------------------------------
series_mode = st.selectbox(
    "Series Seed Rule (global):",
    ["first", "sum", "xor"]
)

st.markdown("---")

# -------------------------------------------------
# Code Specs
# -------------------------------------------------
LETTER_BASE = 26
LETTER_COUNT = LETTER_BASE ** 3
DIGIT_COUNT = 10 ** 5
MAX_SEED = LETTER_COUNT * DIGIT_COUNT - 1

REGEX_FULL_CODE = re.compile(r"^[A-Z]{3}-\d{5}$")
REGEX_PREFIX_ONLY = re.compile(r"^[A-Z]{3}-$")
REGEX_SEED_ONLY = re.compile(r"^\d+$")

PRIME_MODS = [7919, 8923, 9103, 9461, 9721, 9973]

# -------------------------------------------------
# Encode / Decode
# -------------------------------------------------
def encode_seed_to_code(seed: int) -> str:
    letter_index = seed // DIGIT_COUNT
    digits = seed % DIGIT_COUNT

    a = letter_index // (LETTER_BASE**2)
    b = (letter_index // LETTER_BASE) % LETTER_BASE
    c = letter_index % LETTER_BASE
    prefix = "".join(chr(ord("A") + x) for x in (a, b, c))

    return f"{prefix}-{digits:05d}"

def decode_code_to_seed(code: str) -> int:
    prefix, num = code.split("-")
    a = ord(prefix[0]) - ord("A")
    b = ord(prefix[1]) - ord("A")
    c = ord(prefix[2]) - ord("A")
    letter_index = a*LETTER_BASE*LETTER_BASE + b*LETTER_BASE + c
    return letter_index * DIGIT_COUNT + int(num)

# -------------------------------------------------
# Derived mod
# -------------------------------------------------
def derive_mod_from_seed(seed: int) -> int:
    return PRIME_MODS[seed % len(PRIME_MODS)]

# -------------------------------------------------
# Constants from prefix
# -------------------------------------------------
def constants_from_prefix(prefix: str):
    nums = [ord(c) - ord("A") for c in prefix.upper()]
    return {
        "a": 3 + (nums[0] % 7),
        "b": 5 + (nums[1] % 11),
        "c": 7 + (nums[2] % 13),
        "d": 11 + ((nums[0] + nums[1]) % 17),
    }

# -------------------------------------------------
# JSON generator
# -------------------------------------------------
def generate_mse_json(seed: int, prefix: str):
    mod = derive_mod_from_seed(seed)
    constants = constants_from_prefix(prefix)

    v0 = (seed * constants["a"] + constants["b"]) % mod
    v1 = (v0 * constants["c"] + constants["d"]) % mod
    v2 = (v1 * 13 + 17) % mod
    v3 = (v2 * 19 + 23) % mod
    v4 = (v3 * 29 + 31) % mod
    signature = [v0, v1, v2, v3, v4]

    # series seed
    if series_mode == "first":
        sseed = signature[0]
    elif series_mode == "sum":
        sseed = sum(signature) % mod
    else:
        x = 0
        for v in signature:
            x ^= v
        sseed = x % mod

    return {
        "user_id": f"table_{seed}",
        "signature": signature,
        "series_seed": sseed,
        "mod": mod,
        "constants": constants,
    }

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "left_json" not in st.session_state:
    st.session_state.left_json = None
if "right_json" not in st.session_state:
    st.session_state.right_json = None

# -------------------------------------------------
# Layout
# -------------------------------------------------
left, right = st.columns(2)

# -------------------------------------------------
# LEFT PANEL — UNIVERSAL INPUT
# -------------------------------------------------
with left:
    st.subheader("① Input → Code + Seed")

    user_input = st.text_input(
        "Enter seed, prefix-only (AAA-), or full code (AAA-12345):",
        "BSA-"
    )

    seed_value = None
    prefix_value = None
    final_code = None

    if st.button("Generate"):
        try:
            formatted = user_input.strip().upper()

            # CASE 1: Full code
            if REGEX_FULL_CODE.match(formatted):
                prefix_value = formatted.split("-")[0]
                seed_value = decode_code_to_seed(formatted)
                final_code = formatted

            # CASE 2: Prefix-only: ABC-
            elif REGEX_PREFIX_ONLY.match(formatted):
                prefix_value = formatted[:3]

                # We must ask for a seed:
                seed_value = st.number_input(
                    "Enter a seed to pair with prefix:",
                    min_value=0,
                    max_value=MAX_SEED,
                    value=3404
                )
                final_code = f"{prefix_value}-{seed_value % DIGIT_COUNT:05d}"

            # CASE 3: Seed only
            elif REGEX_SEED_ONLY.match(formatted):
                seed_value = int(formatted)
                final_code = encode_seed_to_code(seed_value)
                prefix_value = final_code.split("-")[0]

            else:
                raise ValueError("Invalid input format. Use seed, AAA-, or AAA-12345.")

            # Generate JSON
            mse_json = generate_mse_json(seed_value, prefix_value)

            st.session_state.left_json = {
                "seed": seed_value,
                "prefix": prefix_value,
                "code": final_code,
                "json": mse_json,
            }

        except Exception as e:
            st.error(str(e))

    if st.session_state.left_json:
        st.markdown("### Final Code")
        st.code(st.session_state.left_json["code"])
        st.markdown("### JSON Output")
        st.json(st.session_state.left_json["json"])


# -------------------------------------------------
# RIGHT PANEL — CODE → JSON
# -------------------------------------------------
with right:
    st.subheader("② Code → JSON")

    code_input = st.text_input("Enter Code (AAA-12345):", "BSA-45673")

    if st.button("Decode Code"):
        try:
            code_clean = code_input.strip().upper()
            seed_value = decode_code_to_seed(code_clean)
            prefix_value = code_clean.split("-")[0]

            mse_json = generate_mse_json(seed_value, prefix_value)

            st.session_state.right_json = {
                "seed": seed_value,
                "prefix": prefix_value,
                "code": code_clean,
                "json": mse_json,
            }

        except Exception as e:
            st.error(str(e))

    if st.session_state.right_json:
        st.markdown("### Seed")
        st.code(st.session_state.right_json["seed"])
        st.markdown("### JSON Output (from Code)")
        st.json(st.session_state.right_json["json"])




st.markdown(
    """
        <br><br><br><br><br>
        <div style="text-align:right; font-weight:600; color:#333;">
            Contact: <a href="mailto:jasongdunn@outlook.com">jasongdunn@outlook.com</a>
        </div>
    """,
    unsafe_allow_html=True
)

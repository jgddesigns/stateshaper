from typing import List


def morph_state_default(
    seed: List[int],
    t: int,
    mod: int,
    a: int,
    b: int,
    c: int,
    d: int,
) -> List[int]:
    """Default seed morphing rule.

    new[i] = (a*seed[i] + b*seed[i-1] + c*t + d) mod mod

    - Uses wraparound for the i-1 index.
    - Produces a deterministic, evolving seed with memory.
    """
    n = len(seed)
    new_seed = [0] * n
    for i in range(n):
        left = seed[i - 1]  # wraparound by Python indexing
        center = seed[i]
        new_seed[i] = (a * center + b * left + c * t + d) % mod
    return new_seed

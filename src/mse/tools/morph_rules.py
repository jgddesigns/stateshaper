from typing import List


def morph_state_default(
    state: List[int],
    t: int,
    mod: int,
    a: int,
    b: int,
    c: int,
    d: int,
) -> List[int]:
    """Default state morphing rule.

    new[i] = (a*state[i] + b*state[i-1] + c*t + d) mod mod

    - Uses wraparound for the i-1 index.
    - Produces a deterministic, evolving state with memory.
    """
    n = len(state)
    new_state = [0] * n
    for i in range(n):
        left = state[i - 1]  # wraparound by Python indexing
        center = state[i]
        new_state[i] = (a * center + b * left + c * t + d) % mod
    return new_state

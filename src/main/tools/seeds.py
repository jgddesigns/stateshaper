from typing import List


def fib_seed(n: int = 9) -> List[int]:
    """Return a simple Fibonacci-like seed array of length n."""
    if n <= 0:
        return []
    if n == 1:
        return [1]
    seed = [1, 1]
    while len(seed) < n:
        seed.append(seed[-1] + seed[-2])
    return seed[:n]


def themed_seed_from_word(word: str, length: int = 9) -> List[int]:
    """Map characters of a word to integers (A=1..Z=26) and pad/trim.

    This is useful to create reproducible, human-meaningful seeds like
    themed_seed_from_word("HISTORICAL").
    """
    word = (word or "").upper()
    base = [max(1, min(26, ord(ch) - 64)) for ch in word if ch.isalpha()]
    if not base:
        base = [1]

    # repeat or trim to desired length
    out = []
    i = 0
    while len(out) < length:
        out.append(base[i % len(base)])
        i += 1
    return out[:length]

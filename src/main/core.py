from typing import List, Dict, Sequence
from tools.morph_rules import morph_state_default
from tools.semantic_mapper import SemanticMapper


class MorphicSemanticEngine:
    """Core engine: evolves a numeric state and emits semantic tokens.

    This class is intentionally simple and opinionated:
    - It keeps track of a fixed-length integer state.
    - On each step, it morphs the state using a deterministic rule.
    - It converts the state into an integer code.
    - A SemanticMapper turns codes into tokens from a vocabulary.
    """

    def __init__(
        self,
        seed: Sequence[int],
        vocab: Sequence[str],
        constants: Dict[str, int] = None,
        mod: int = 9973,
    ) -> None:
        if not seed:
            raise ValueError("seed must be non-empty")
        if not vocab:
            raise ValueError("vocab must be non-empty")

        self.seed = [int(x) % mod for x in seed]
        self.vocab = vocab
        self.constants = {
            "a": 3,
            "b": 5,
            "c": 7,
            "d": 11,
        } if not constants else constants
        self.mod = mod
       
        self.t = 0  # iteration counter

        self.mapper = SemanticMapper(vocab=vocab)
        self._prev_token_index = 0

        self.seed_format = {
            "seed": None,
            "vocab": None,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }, 
            "mod": 9973
        }
    # ---------------------------
    # Core stepping logic
    # ---------------------------
    def _base_code(self) -> int:
        """Aggregate state into a small integer code (0..26 by default).

        This mixes position and value to provide a stable but evolving summary.
        """
        total = 0
        for i, val in enumerate(self.seed):
            total += (i + 1) * val
        return (total + self.t) % 27

    def _offset(self) -> int:
        """Compute an offset based on the current state sum.

        This helps keep mapping dynamic even if base_code repeats.
        """
        return sum(self.seed) % len(self.mapper.vocab)


    #based on the seed, morphs the array and gets a token from the vocab.
    def step(self) -> str:
        """Advance the engine by one step and return the next token."""
        base = self._base_code()
        offs = self._offset()
        idx = (base + offs + self._prev_token_index) % len(self.mapper.vocab)

        token = self.mapper.index_to_token(idx)
        self._prev_token_index = idx

        # evolve state deterministically
        self.seed = morph_state_default(
            seed=self.seed,
            t=self.t,
            mod=self.mod,
            **self.constants,
        )
        self.t += 1
        return token

    def next_token(self) -> str:
        """Alias for step() to make intent clearer in examples."""
        return self.step()

    def generate_tokens(self, n: int) -> List[str]:
        """Generate a list of n tokens."""
        return [self.step() for _ in range(n)]
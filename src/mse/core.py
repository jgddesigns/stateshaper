from typing import List, Dict, Sequence
from .morph_rules import morph_state_default
from .classes.SemanticMapper import SemanticMapper


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
        initial_state: Sequence[int],
        vocab: Sequence[str],
        constants: Dict[str, int],
        mod: int = 9973,
    ) -> None:
        if not initial_state:
            raise ValueError("initial_state must be non-empty")
        if not vocab:
            raise ValueError("vocab must be non-empty")
        print("start")
        self.mod = mod

        self.seed = self.build_seed(initial_state)
        self.state = [int(x) % mod for x in self.seed]
        self.t = 0  # iteration counter

        self.constants = {
            "a": int(constants.get("a", 3)),
            "b": int(constants.get("b", 5)),
            "c": int(constants.get("c", 7)),
            "d": int(constants.get("d", 11)),
        }

        self.mapper = SemanticMapper(vocab=vocab)
        print("after mapper")
        self._prev_token_index = 0

    # ---------------------------
    # Core stepping logic
    # ---------------------------
    def _base_code(self) -> int:
        """Aggregate state into a small integer code (0..26 by default).

        This mixes position and value to provide a stable but evolving summary.
        """
        total = 0
        for i, val in enumerate(self.state):
            total += (i + 1) * val
        return (total + self.t) % 27

    def _offset(self) -> int:
        """Compute an offset based on the current state sum.

        This helps keep mapping dynamic even if base_code repeats.
        """
        return sum(self.state) % len(self.mapper.vocab)


    def step(self) -> str:
        """Advance the engine by one step and return the next token."""

        base = self._base_code()
        offs = self._offset()
        idx = (base + offs + self._prev_token_index) % len(self.mapper.vocab)
        token = self.mapper.index_to_token(idx)
        self._prev_token_index = idx
        self.state = morph_state_default(
            state=self.state,
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


    ### build initial seed to create the initial state
    def build_seed(self, signature, base_array=None, iterations=5):
            if base_array is None:
                base_array = [676, 612, 550, 490, 432, 376, 322, 270, 220]

            arr = base_array[:]
            h, c, st, strn, life = signature

            for i in range(iterations):
                for idx in range(len(arr)):
                    delta = (h - c) + (strn - st) + life + i
                    arr[idx] = (arr[idx] + delta + idx * h) % 9973  # match your mod

            return arr  # this becomes initial_state / seed
    
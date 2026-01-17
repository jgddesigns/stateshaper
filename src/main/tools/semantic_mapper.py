from typing import Sequence


class SemanticMapper:
    """Maps integer indices to tokens from a fixed vocabulary."""

    def __init__(self, vocab: Sequence[str]) -> None:
        if not vocab:
            raise ValueError("vocab must be non-empty")
        self.vocab = list(vocab)

    def index_to_token(self, idx: int) -> str:
        return self.vocab[idx % len(self.vocab)]

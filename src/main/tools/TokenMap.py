class TokenMap:
    """Maps integer indices to tokens from a fixed vocabulary."""

    def __init__(self, vocab):
        if not vocab:
            raise ValueError("vocab must be non-empty")
        self.vocab = list(vocab)

    def get_token(self, idx):
        return self.vocab[idx]
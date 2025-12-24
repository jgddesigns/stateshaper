import sys
from typing import List, Dict, Sequence
from tools.Morph import Morph
from tools.TokenMap import TokenMap


class Stateshaper:

    def __init__(
        self,
        seed: Sequence[int],
        vocab: Sequence[str],
        constants: Dict[str, int] = None,
        mod: int = 9973,
        compound: list = None, 
    ) -> None:
        if not seed:
            raise ValueError("seed must be non-empty")
        if not vocab:
            raise ValueError("vocab must be non-empty")

        self.token_map = TokenMap(vocab)
        self.morph = Morph()

        self.seed = [int(x) % mod for x in seed]

        self.original_seed = [int(x) % mod for x in seed]
    
        self.vocab = vocab
        self.constants = {
            "a": 3,
            "b": 5,
            "c": 7,
            "d": 11,
        } if not constants else constants
        self.mod = mod
        self.compound = compound
       
        self.iteration = 1 

        self.prior_index = 0

        self.seed_format = {
            "seed": self.seed,
            "vocab": self.vocab,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }, 
            "mod": 9973
        }

        if compound:
            self.seed_format["compound"] = compound

        self.token_array = []


    def base_index(self):
        total = 0
        for i, val in enumerate(self.seed):
            total += (i + 1) * val
        return (total + self.iteration) % 17


    def get_index(self):
        return int(sum(self.seed)/len(self.vocab)) % len(self.vocab)


    def next_token(self, n, forward=True):
        if self.iteration < 0:
            self.seed = self.original_seed

        index = self.get_index()

        token = self.token_map.get_token(index) if not self.compound_token else self.compound_token(index)

        self.seed = self.morph.morph(self.seed_format, self.iteration) if self.iteration < n or forward == False else self.seed

        self.token_array.append(self.seed[0])

        if forward == True:
            self.iteration += 1  
        else:
            self.iteration -= 1

        return token
    

    def compound_token(self, index):
        compounds = [self.token_map.get_token(index)]
        while len(compounds) < self.compound[0]:
            index = (index + self.compound[1]) % len(self.vocab)
            if self.token_map.get_token(index) not in compounds:
                compounds.append(self.token_map.get_token(index))
            else:
                index = index + self.compound[1]

        return self.compound_term(index, compounds)
    

    def compound_term(self, index, compounds):
        terms = []
        tokens = []

        while len(terms) < len(compounds)-1:
            terms.append(self.compound[2][(index + len(terms)) % len(self.compound[2])])

        length = len(terms) + len(compounds)

        while len(tokens) < length:
            tokens.append(compounds[0])
            compounds.pop(0)
            if len(terms) > 0:
                tokens.append(terms[0]) 
                terms.pop(0)

        return " ".join(tokens)
    

    def generate_tokens(self, n):
        """Generate a list of n tokens."""
        return [self.next_token(n) for _ in range(n)]
    

    def reverse_tokens(self, n):
        """Generate a list of n tokens."""
        self.iteration -= 3

        return [self.next_token(n, False) for _ in range(n)]
    

    def get_array(self, length=50):
        self.generate_tokens(length)
        return self.token_array 
    

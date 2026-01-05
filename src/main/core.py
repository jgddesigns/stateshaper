import sys
from typing import List, Dict, Sequence
from tools.Morph import Morph
from tools.TokenMap import TokenMap


class Stateshaper:

    def __init__(self, seed, vocab, constants={"a": 3, "b": 5, "c": 7, "d": 11}, mod=9973, compound=None):
        if not seed:
            raise ValueError("seed must be non-empty")
        if not vocab:
            raise ValueError("vocab must be non-empty")

        self.token_map = TokenMap(vocab)
        self.morph = Morph()

        self.seed = [int(x) % mod for x in seed]

        self.original_seed = [int(x) % mod for x in seed]
    
        self.vocab = vocab
        self.constants = constants
        self.mod = mod
        self.compound = compound
       
        self.iteration = 1 

        self.prior_index = 0

        self.seed_format = {
            "seed": self.seed,
            "vocab": self.vocab,
            "constants": self.constants,
            "mod": self.mod
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

        token = self.token_map.get_token(index) if not self.compound else self.compound_token(index)

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
        self.generated_tokens = [self.next_token(n) for _ in range(n)]
        return self.generated_tokens


    def retrieve_token(self, pos):
        return self.generated_tokens[pos-1]


    def reverse_tokens(self, n):
        self.iteration -= 3
        return [self.next_token(n, False) for _ in range(n)]
    

    def get_array(self, length=50):
        self.generate_tokens(length)
        return self.token_array 
    
    
    # jumps to spot in array. 
    # index is actual place in the array (0 not included). if 50 tokens were created, enter 50 to get the 50th token and 1 to get the first token. 
    def jump(self, index):
        self.rebuild()
        if index > 0:
            tokens = [self.next_token(index) for _ in range(index)] 
        try:
            return tokens[index-1]
        except:
            raise ValueError("Error in 'Stateshaper' class, 'jump' function. Can't find position in token stream. Please check the parameter value and try again.\n") 
        

    def jump_back(self, index):
       if index >= self.iteration:
           raise ValueError(f"Error in 'Stateshaper' class, 'jump_back' function. Jump back index '{index}' is greater than current iteration.\n") 
       back = list(reversed(self.reverse_tokens(self.iteration - index)))
       self.iteration += 3
       return back[0]


    def rebuild(self):
        self.seed = self.original_seed
        self.iteration = 1
        self.prior_index = 0
        self.token_array = []

import sys


class Stateshaper:

    def __init__(self, state=5, vocab=[], constants={"a": 3, "b": 5, "c": 7, "d": 11}, mod=9973, compound=None):

        if isinstance(state, int) == False:
            self.current_state = [int(x) % mod for x in state]
            self.original_state = [int(x) % mod for x in state]
        else:
            self.current_state = state
            self.original_state = state
    
        self.current_vocab = vocab
        self.original_vocab = vocab
        self.constants = constants
        self.mod = mod
        try:
            compound[0] = [compound[0]] if isinstance(compound[0], int) == True else compound[0] if compound else None
        except:
            pass
        self.compound = compound
        print(compound)
        
       
        self.iteration = 1 

        self.prior_index = 0

        self.seed_format = {
            "state": self.current_state,
            "vocab": self.original_vocab,
            "constants": self.constants,
            "mod": self.mod
        }

        if compound:
            self.seed_format["compound"] = compound

        self.token_array = []




    def step(self): 
        self.morph_array()
        self.iteration += 1
        return self.get_token() if not self.compound else self.compound_token()


    def reverse(self):
        if self.iteration > 1:
            value = self.current_state[len(self.current_state)-1]
            self.iteration = self.iteration - 1
            self.current_state = self.current_state[:len(self.current_state)-1] 
            old_value = [self.reverse_morph(value)]
            self.current_state = old_value + self.current_state
        return self.get_token() if not self.compound else self.compound_token()


    def get_token(self):
        return self.current_vocab[self.index_token()] if len(self.current_vocab) > 0 else self.current_state[0]
    

    def generate_tokens(self, amount):
        self.rebuild()
        return [self.step() for _ in range(amount)]
    

    def index_token(self):
        return self.current_state[0] * (self.constants["a"] * (self.constants["c"] + self.constants["b"])) % len(self.current_vocab)


    def morph_array(self):
        value = self.current_state[0]
        self.current_state = self.current_state[1:]
        self.current_state.append(self.new_value(value))


    def reverse_morph(self, value):
        return ((value - self.constants["d"]) * pow((round((self.constants["c"] * self.constants["c"]) / self.constants["a"]) * self.constants["b"] * self.iteration) % self.mod, -1, self.mod)) % self.mod


    def new_value(self, value):
        return self.morph_logic(value) 


    def morph_logic(self, value):
        return (self.constants["d"] + round((self.constants["c"] * self.constants["c"])/self.constants["a"]) * self.constants["b"] * self.iteration * value) % self.mod
    

    def jump(self, index):
        self.rebuild()
        tokens = [self.step() for _ in range(index)]
        return tokens[len(tokens)-1]


    def rebuild(self): 
        self.iteration = 1
        self.current_state = self.original_state


    def compound_token(self):
        count = 0
        tokens = []

        current = self.compound[0][self.current_state[0] * (self.constants["c"] if self.current_state[0] % 3 == 0 else self.constants["b"]) % len(self.compound[0])]
        group = self.current_vocab[(self.current_state[0] * self.constants["b"] if self.current_state[0] * self.current_state[0] * self.constants["d"] % 3 == 0 else self.current_state[0] * self.constants["d"]) % len(self.current_vocab)]
        
        while (len(tokens) < current and current < len(group)) or (len(tokens) < len(group) and current >= len(group)):
            token = group[(self.current_state[0] + count + self.iteration * (len(tokens)*self.constants["c"]) * (self.constants["a"] * (self.constants["c"] + self.constants["b"]))) % len(group)] 
            if token in tokens:
                count += 1
            else:
                tokens.append(token) 
        i = 1
        while i < len(tokens):
            tokens.insert(i, self.compound[2][((len(tokens) + 1) * self.iteration * self.constants["c"]) % len(self.compound[2])])
            i += 2

        return " ".join(tokens)
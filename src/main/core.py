
class Stateshaper:

    def __init__(self, state=[10, 67, 876, 347, 19], vocab=[], constants={"a": 3, "b": 5, "c": 7, "d": 11}, mod=9973, compound=None):

        self.current_state = [int(x) % mod for x in state]

        self.original_state = [int(x) % mod for x in state]
    
        self.current_vocab = vocab
        self.original_vocab = vocab
        self.constants = constants
        self.mod = mod
        self.compound = compound
       
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
        self.iteration = self.iteration - 1 if self.iteration > 1 else 1
        value = self.current_state[len(self.current_state)-1]
        self.current_state = self.current_state[:len(self.current_state)-1]
        old_value = [self.reverse_morph(value)]
        self.current_state = old_value + self.current_state
        return self.get_token()


    def get_token(self):
        return self.current_vocab[self.index_token()]
    

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
        tokens = []
        count = 0
        while len(tokens) < self.compound[0]:
            token = self.current_vocab[(self.current_state[0] + count + self.iteration * (len(tokens)*self.constants["c"]) * (self.constants["a"] * (self.constants["c"] + self.constants["b"]))) % len(self.current_vocab)] 
            if token in tokens:
                count += 1
            else:
                tokens.append(token) 
        i = 1
        while i < len(tokens):
            tokens.insert(i, self.compound[2][((len(tokens) + 1) * self.iteration * self.constants["c"]) % len(self.compound[2])])
            i += 2

        return " ".join(tokens)
    

    def compound_reverse(self):
        pass
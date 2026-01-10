import random
import sys
from connector.Connector import Connector
from core import Stateshaper
from tools.derive_vocab.DeriveVocab import DeriveVocab
from tools.tiny_state.TinyState import TinyState
from example_data.format_data.FormatData import FormatData



class RunEngine:

    def __init__(self, data=None, seed=None, token_count=10, initial_state=[66, 67, 54, 3, 34], vocab=None, constants={"a": 3,"b": 5,"c": 7,"d": 11}, mod=9973, **kwargs):
        super().__init__(**kwargs)

        if isinstance(data, dict):
            self.data = data
        else:
            print("Data is not formatted or formatted incorrectly. See accepted data formats in the 'example_data' directory.")
            sys.exit()

        self.seed = None

        if isinstance(seed, dict):
            try:
                initial_state = seed["s"] 
            except:
                initial_state = initial_state 
            try:
                vocab = seed["v"]
            except:
                vocab = vocab
            try:
                constants = seed["c"]
            except:
                constants = constants
            try: 
                mod = seed["m"] 
            except: 
                mod = mod
        
            self.seed = {
                "state": initial_state,
                "vocab": vocab,
                "constants": constants,
                "mod": mod
            }

        print(self.seed)
        self.connector = Connector(self.data, token_count=token_count, initial_state=initial_state,  constants=constants, vocab=vocab, mod=mod)


        self.tiny_state = TinyState()

        self.format_data = FormatData()

        self.derive_vocab = DeriveVocab()

        self.engine = None

        self.default_seed = None

        self.derived_seed = None




    def start_engine(self):
        self.engine = None
        self.seed = self.connector.start_connect()
        self.define_engine()


    def define_engine(self):
        self.engine = Stateshaper(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"],
            [self.data["compound_length"], self.data["compound_modifier"], self.data["compound_terms"]] if self.data["rules"] == "compound" else None
        )


    def run_engine(self, token_count=None):
        print(self.seed)
        self.tokens = self.engine.generate_tokens(self.connector.token_count if not token_count else token_count)
        
        print("\n\nTokens successfully generated from vocab.")
        print("============================================")
        print(self.tokens)

        return self.tokens
    

    def reverse(self):
        self.tokens = self.engine.reverse()

        print("\n\nToken re-created from reverse.")
        print("============================================")
        print(self.tokens)

    
    
    def jump(self, index):
        self.tokens = self.engine.jump(index)

        print(f"\n\nToken successfully accessed from index {str(index)}.")
        print("============================================")
        print(self.tokens)


    def rebuild(self):
        self.engine.rebuild()


    def get_seed(self, vocab=False):
        return self.connector.output_seed(vocab)
    
    def get_derived(self):
        return self.derived_seed
    

    def adjust_ratings(self):
        for _ in range(20):
            self.derive_vocab.adjust_rankings(self.test_input(), self.data)
        new_vocab = self.derive_vocab.current_vocab()
        self.seed["vocab"]  = new_vocab
        self.derived_seed = self.new_seed(new_vocab)
        self.define_engine()


    def new_seed(self, vocab):
        seed = {}

        seed["s"] = self.seed["state"]  
        seed["v"] = self.connector.compress_regular(vocab)
        seed["c"] = self.seed["constants"]
        seed["m"] = self.seed["mod"]

        self.derived_seed = seed["v"]  

        return seed
    

    def test_input(self):
        input = []
        keys = [list(i.keys())[0] for i in self.data["input"]]
        while len(input) < 20:     
            answer = random.choice([True, False])
            input.append([answer, [random.choice(keys), random.choice(keys), random.choice(keys)]])

        return input
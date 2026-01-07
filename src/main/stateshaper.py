import sys
from connector.Connector import Connector
from core import Stateshaper
from tools.tiny_state.TinyState import TinyState




class RunEngine:

    def __init__(self, data=None, seed=None, token_count=10, initial_state=[66, 67, 54, 3, 34],constants={"a": 3,"b": 5,"c": 7,"d": 11}, mod=9973, **kwargs):
        super().__init__(**kwargs)

        if isinstance(data, dict):
            self.data = data
        else:
            print("Data is not formatted or formatted incorrectly. See accepted data formats in the 'example_data' directory.")
            sys.exit()

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


        self.connector = Connector(self.data, token_count=token_count, initial_state=initial_state, vocab=vocab, constants=constants, mod=mod)

        self.tiny_state = TinyState()

        self.engine = None
        self.seed = None
        self.default_seed = None




    def start_engine(self):
        self.seed = self.connector.start_connect() if not self.seed else self.default_seed
        self.default_seed = self.seed if not self.default_seed else self.default_seed
        self.define_engine()


    def define_engine(self):
        self.engine = Stateshaper(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"],
            [self.data["compound_length"], self.data["compound_modifier"], self.data["compound_terms"]] if self.data["rules"] == "compound" else None
        )


    def run_engine(self):
        self.tokens = self.engine.generate_tokens(self.connector.token_count)
        
        print("\n\nTokens successfully generated from vocab.\n")
        print(self.tokens)

        return self.tokens
    

    def rebuild(self):
        self.engine.rebuild()


    def get_seed(self, vocab=False):
        return self.connector.output_seed(vocab)
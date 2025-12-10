from Vocab import Vocab
import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

class Connector:


    def __init__(self, data=None, token_count=10, constants=None, mod=None, **kwargs):
        super().__init__(**kwargs)

        self.debug = True

        self.default_mod = 9973
        self.default_constants = {
            "a": 3,
            "b": 5,
            "c": 7,
            "d": 11
        }

        self.engine = None
        self.state = None
        self.vocab = None
        self.constants = constants if constants else self.default_constants
        self.mod = mod if mod else self.default_mod

        self.vocab = None
        self.data = data 
        self.token_count = token_count

        if data and isinstance(data, dict) == False and isinstance(data, list) == False: 
            print("\nData input is invalid. The input requires 'dict' or 'list' format.")

        if constants and (isinstance(constants, list) == False or len([i for i in constants if isinstance(i, int) == False] > 0)):
            print("\nConstants parameter is invalid. It needs to be a list containing integer values.")

        self.start_connect()


    def start_connect(self):
        self.build_seed()
        self.engine = {
            "state": self.state,
            "vocab": self.vocab,
            "constants": self.constants,
            "mod": self.mod
        }

        print("\n\n\nMSE Seed has been created:\n")
        print(self.engine)
        print("\n")

        return self.engine


    def build_seed(self):
        self.vocab = self.get_vocab()
        self.state = self.get_state()


    def get_vocab(self):
        if isinstance(self.data, dict):
            self.vocab = Vocab(self.data)  
            return self.vocab.define_vocab()
        else:   
            self.vocab = Vocab()  
            self.vocab.test()
        

    def get_state(self):
        return [66, 67, 54, 3, 34]


    def get_constants(self):
        if not self.constants:
            self.constants = self.default_constants


    def assign_constants(self, constants=None):
        new_constants = {}
        for key in self.default_constants.keys():
            new_constants[key] = constants[len(new_constants)] if constants else None
        return new_constants if constants else self.default_constants
        

    def get_mod(self):
        if not self.mod:
            self.mod = self.default_mod  


    def change_data(self, data):
        self.data = data


    def change_token(self, token):
        self.token_count = token



    

Connector()
import random
import sys
from tools.tiny_state.TinyState import TinyState
from .Vocab import Vocab
from .Modify import Modify




class Connector:


    def __init__(self, data, token_count=10, initial_state=None, constants=None, vocab=None, mod=None, **kwargs):
        
        if data["rules"] == "rating":
            data["length"] = len(data["input"]) if data["length"] > len(data["input"]) else data["length"]

        self.debug = True
        self.modify = Modify(data)
        self.tiny_state = TinyState()

        self.initial_state = initial_state
        self.default_constants = {
            "a": 3,
            "b": 5,
            "c": 7,
            "d": 11
        }
        self.default_mod = 9973

        self.engine = None
        self.state = None
        self.vocab = vocab if vocab else None
        self.compressed_vocab = None
        self.constants = constants if constants else self.default_constants
        self.mod = mod if mod else self.default_mod

        self.token_count = token_count

        self.compressed_seed = None

        self.check_input(data, constants)

        self.check_random(data)

        self.check_compound(data)

        self.data = data

        self.vocab_rules = {
            "rating": self.get_personalization,
            "random": self.get_data,
            "compound": self.get_data,
            "tokens": self.get_tokens
        }



    def start_connect(self, format=None):
        self.build_seed()
        
        self.engine = self.minimal_seed = {
            "state": self.state,
            "vocab": self.vocab,
            "constants": self.constants,
            "mod": self.mod
        }

        print("\n\n\nStateshaper Seed has been created:\n")
        print(self.engine)

        print("\n\n\nVocab is Compressed:\n")
        print(self.compressed_vocab)

        print("\n\n\nFull Seed:\n")
        self.engine["vocab"] = self.compressed_vocab if format else self.engine["vocab"]

        self.output_seed()

        print("\n\n\nMinimal Output Seed:\n")
        self.compressed_seed["v"] = self.compressed_vocab
        print(self.compressed_seed)
        print("\nSize: " + str(len(str(self.compressed_seed))) + " bytes\n\n\n")
        
        return self.engine
    


    def output_seed(self, state=None, vocab=None, constants=None, mod=None, derived=None):
        seed = {}

        seed["s"] = self.engine["state"] if not state else state
        seed["v"] = self.compressed_vocab if vocab == True else derived if derived else ""
        seed["c"] = self.engine["constants"] if not constants else constants
        seed["m"] = self.engine["mod"] if not mod else mod

        self.compressed_seed = seed  

        return seed


    def check_input(self, data, constants):
        if data and isinstance(data, dict) == False and isinstance(data, list) == False: 
            print("\nData input is invalid. The input requires 'dict' or 'list' format.")

        if constants and (isinstance(constants, dict) == False or len([constants[i] for i in list(constants.keys()) if isinstance(constants[i], int) == False]) > 0):
            print("\nConstants parameter is invalid. It needs to be a dict with keys containing integer values.")

        try:
            isinstance(data["length"], int)
        except:
            data["length"] = 10



    def check_random(self, data):
        try:
            isinstance(data["rules"], str) and data["rules"] == "random"
        except:
            data["rules"] = "random"
            return True
        
        try:
            isinstance(data["modifier"], int)
        except:
            data["modifier"] = 21
            

    def check_compound(self, data):
        try:
            isinstance(data["rules"], str) and data["rules"] == "compound"
        except:
            data["rules"] = "random"
            return True
        
        try:
            isinstance(data["compound_modifier"], int)
        except:
            data["compound_modifier"] = 7

        try:
            isinstance(data["compound_length"], int)
        except:
            data["compound_length"] = 3

        try:
            isinstance(data["compound_groups"], list)
        except:
            data["compound_groups"] = None

        try:
            isinstance(data["compound_terms"], list)
        except:
            data["compound_terms"] = [" "]


    def build_seed(self):
        if self.vocab:
            self.compressed_vocab = self.vocab
            self.vocab = self.vocab_rules[self.data["rules"]](self.vocab[0], self.vocab[1], self.data) if self.data["rules"] != "tokens" else []
        else:
            self.vocab = self.get_vocab() if self.data["rules"] != "tokens" else []
            self.compressed_vocab = self.compress_vocab() if self.data["rules"] != "tokens" else []
        self.state = self.initial_state
        self.constants = self.default_constants
        self.mod = self.default_mod


    def get_constants(self):
        values = ["a", "b", "c", "d"]
        constants = {}
        assigned = 1
        for value in values:
            constant = random.randint(assigned + 1, assigned + 10)
            constants[value] = constant
            assigned = constant

        return constants


    def get_vocab(self):
        if self.vocab:
            return True
        if isinstance(self.data, dict):
            self.vocab_obj = Vocab(self.data)  
            return self.vocab_obj.define_vocab() 
        else:   
            print("no valid data")


    def get_state(self):
        return self.initial_state


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


    def set_value(self, key, rating):
        self.modify.modify(key, rating)


    def adjust_value(self, key, adjust):
        self.modify.adjust(key, adjust)


    def compress_vocab(self, vocab=None):
        return self.tiny_state.get_seed(self.data, self.vocab if not vocab else vocab)


    def compress_regular(self, vocab=None):
        return self.tiny_state.derived_seed(self.data, self.vocab if not vocab else vocab)
    

    def get_minimal(self):
        return self.compressed_seed
    

    def decode_seed(self, seed):
        return self.tiny_state.decode(seed)


    def decode_minimal(self, seed, minimal):
        return self.tiny_state.decode_subset_seed(seed, minimal)


    def get_personalization(self, seed, minimal, data):
        return self.tiny_state.rebuild_data(seed, minimal, data)


    def get_data(self, seed, minimal, data):
        return self.tiny_state.rebuild_regular(seed, minimal, data)
    

    def get_tokens(self, seed, minimal, data):
        return []
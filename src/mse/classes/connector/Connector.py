



from mse.classes.connector.Vocab import Vocab


class Connector:


    def __init__(self, data=None, token_count=30, constants=None, mod=None, **kwargs):
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
        self.constants = constants
        self.mod = mod

        self.vocab = None
        self.data = data 
        self.token_count = token_count

        if data and isinstance(data, dict) == False: 
            print("\nData input is invalid. The input requires 'dict' format.")

        elif constants and (isinstance(constants, list) == False or len([i for i in constants if isinstance(i, int) == False] > 0)):
            print("\nConstants parameter is invalid. It needs to be a list containing integer values.")

        else:
            self.start_connect()




    def start_connect(self):
        self.build_seed()

        self.engine = {
            "state": self.state,
            "vocab": self.vocab,
            "constants": self.constants,
            "mod": self.mod
        }

        return self.engine


    def build_seed(self):
        self.vocab = self.get_vocab()
        self.state = self.get_state()
        self.constants = self.get_constants()
        self.mod = self.get_mod()


    def get_state(self):
        return [66, 5, 354, 3, 34]


    def get_vocab(self):
        self.vocab = Vocab(self.data)
        return self.vocab.define_vocab()

    def get_constants(self):
        if not self.constants:
            self.constants = self.assign_constants()


    def assign_constants(self, constants):
        new_constants = {}
        for key in self.default_constants.keys():
            new_constants[key] = constants[len(new_constants)]
        return new_constants
        

    def get_mod(self):
        if not self.mod:
            self.mod = self.default_mod  


    def change_data(self, data):
        self.data = data


    def change_token(self, token):
        self.token_count = token



    

# Connector()
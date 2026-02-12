from core import Stateshaper


class RunEngine:

    def __init__(self, initial_state=158, constants={"a": 4,"b": 9,"c": 515,"d": 1171}, mod=489489489418948948942894284273, **kwargs):
        self.initial_state = initial_state
        self.constants = constants
        self.mod = mod

        self.start_engine()
        self.jump(10000000000000000000000000000000000000000000000000000000)


    def start_engine(self):
        self.engine = None
        self.define_engine()


    def define_engine(self, initial_state=None, constants=None, mod=None):
        self.engine = Stateshaper(
            initial_state = self.initial_state if not initial_state else initial_state,
            constants = self.constants if not constants else constants,
            mod = self.mod if not mod else mod
        )


    def run_engine(self, token_count=10):
        self.tokens = self.engine.generate_tokens(token_count)
        print("\n\nTokens successfully generated from vocab.")
        print("============================================")
        print(self.tokens)
        return self.tokens
    

    def reverse(self, token_count=10):
        self.tokens = [self.engine.reverse() for _ in range(token_count)]
        print("\n\nToken re-created from reverse.")
        print("============================================")
        print(self.tokens)
        return self.tokens

    
    def jump(self, index):
        self.tokens = self.engine.jump(index)
        print(f"\n\nToken successfully accessed from index {str(index)}.")
        print("============================================")
        print(self.tokens)
        return self.tokens


    def one_token(self):
        self.tokens = self.engine.step()
        print("\n\nOne token has been created.")
        print("============================================")
        print(self.tokens)
        return self.tokens 
    

    def reverse_one(self):
        self.tokens = self.engine.reverse() 
        print("\n\nOne token re-created from reverse.")
        print("============================================")
        print(self.tokens)
        return self.tokens
    

RunEngine()
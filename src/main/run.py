from demo import Demo
from connector.Connector import Connector
from core import Stateshaper
from tests.Tests import Tests
from tools.tiny_state.TinyState import TinyState




class RunEngine:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin = Demo()
        self.data = self.plugin.compound_test()
        self.vocab_test = self.plugin.vocab_test()

        self.connector = Connector(self.data)

        self.tests = Tests()
        self.tests.debug = True

        self.tiny_state = TinyState()

        self.engine = None

        self.seed = None
        self.compressed_seed = None

        # self.tiny_state.get_seed(self.data, self.vocab_test)
        self.connector.start_connect()


    def run_engine(self):
        self.seed = self.connector.start_connect()

        try:
            self.compressed_seed = self.compress_seed() if self.data["rules"] == "rating" else None
        except:
            pass

        self.define_engine()

        self.tokens = self.engine.generate_tokens(self.connector.token_count)
        
        print("\n\nTokens successfully generated from vocab.\n")
        print(self.tokens)

        self.run_tests()


    def run_tests(self):
        self.define_engine()

        self.tests.determinism({"compare": "stateshaper", "run": self.engine.generate_tokens}, self.connector.token_count, self.tokens)

        self.define_engine()

        self.tests.reversibility({"compare": "stateshaper", "forward": self.engine.generate_tokens, "reverse": self.engine.reverse_tokens}, self.connector.token_count)


    def define_engine(self):
        self.engine = Stateshaper(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"],
            [self.data["compound_length"], self.data["compound_modifier"], self.data["compound_terms"]] if self.data["rules"] == "compound" else None
        )

        
    def compress_seed(self):
        tiny_state = TinyState()
        tiny_state.get_seed(self.data["input"])


RunEngine()
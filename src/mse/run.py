from .classes.connector.Connector import Connector

from .core import MorphicSemanticEngine
from .plugins.ads.Ads import Ads



class RunEngine:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin = Ads()
        self.connector = Connector(self.plugin.get_data())

        self.engine = None

        self.seed = None
        self.compressed_seed = None

        # self.asdf = "asdf"
        self.run_engine()


    def run_engine(self):
        self.seed = self.connector.start_connect()
        self.compressed_seed = self.compress_seed()
        self.engine = MorphicSemanticEngine(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"],
        )

        self.tokens = self.engine.generate_tokens(self.connector.token_count)
        

        print("\n\nTokens successfully generated from vocab.\n")
        # print(self.tokens)
        # print("\n\nSeed:\n")
        # print(self.seed)
        # print("\n\nRunning engine...\n")
        # i = 0
        # while i < 5:
        #     self.engine.step()
        #     i+=1

    def test(self):
        pass


    def test_data(self):
        print("\n\nRunning test function from run class.")
        return {
            "input": [
                {
                    "data": "asdf",
                    "rating": 14
                }, 
                {
                    "data": "asdf",
                    "rating": 14
                }, 
                {
                    "data": "asdf",
                    "rating": 14
                }, 
                {
                    "data": 123,
                    "rating": 45,
                },
                {
                    "data": 456,
                    "rating": 88,
                },
                {
                    "data": 789,
                    "rating": 35,
                },
                {
                    "data": 1673,
                    "rating": 75,
                },
                {
                    "data": 1238,
                    "rating": 65,
                },
                {
                    "data": 1213,
                    "rating": 25,
                },
                {
                    "data": 4526,
                    "rating": 92,
                },
                {
                    "data": 7849,
                    "rating": 3,
                },
                {
                    "data": 1073,
                    "rating": 55,
                },
                {
                    "data": 18,
                    "rating": 77,
                },
            ],
            
            "rules": "rating",
            "length": 10,
            "compound_length": 3,
            "compound_rules": "dfdfdf"
        }
    
    def compress_seed(self):
        self.seed["vocab"] = [self.plugin.compressed_vocab, self.plugin.subset_seed]


# RunEngine()
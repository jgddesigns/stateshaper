from classes.connector.Connector import Connector

from mse.core import MorphicSemanticEngine



class RunEngine:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connector = Connector(self.test_data)

        self.engine = None

        self.engine_data = None

        self.run_engine()


    def run_engine(self):
        self.engine_data = self.connector.start_connect()

        self.engine = MorphicSemanticEngine(
            self.engine_data["state"],
            self.engine_data["vocab"],
            self.engine_data["constants"],
            self.engine_data["mod"],
        )

        self.tokens = self.engine.generate_tokens(self.connector.token_count)

        print(self.tokens)


    def test(self):
        # self.define_vocab(self.data["rules"])
        pass


    def test_data(self):
        print("\n\nRunning test function from Vocab class.")
        return {
            "input": [
                {
                    "data": "asdf",
                    "rank": 14
                }, 
                {
                    "data": "asdf",
                    "rank": 14
                }, 
                {
                    "data": "asdf",
                    "rank": 14
                }, 
                {
                    "data": 123,
                    "rank": 45,
                },
                {
                    "data": 456,
                    "rank": 88,
                },
                {
                    "data": 789,
                    "rank": 35,
                },
                {
                    "data": 1673,
                    "rank": 75,
                },
                {
                    "data": 1238,
                    "rank": 65,
                },
                {
                    "data": 1213,
                    "rank": 25,
                },
                {
                    "data": 4526,
                    "rank": 92,
                },
                {
                    "data": 7849,
                    "rank": 3,
                },
                {
                    "data": 1073,
                    "rank": 55,
                },
                {
                    "data": 18,
                    "rank": 77,
                },
            ],
            
            "rules": "token",
            "length": 10,
            "compound_length": 3,
            "compound_rules": "dfdfdf"
        }
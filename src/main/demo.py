
from demos.markov.Markov import Markov
from connector.Connector import Connector


class Demo:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.markov = Markov()
        self.connector = None

        self.connector_test()


    def markov_test(self):
        self.markov.reverse_test(50, 10, False)
        self.markov.reverse_test(50, 10)
        self.markov.deterministic_test(10, 10, False)
        self.markov.deterministic_test(10, 10)
        self.markov.compression_test(100)
        self.markov.compression_test(50)
        self.markov.compression_test(25)
        self.markov.compression_test(10)


    def connector_test(self):
        data = {
            "input": [
                {
                    "data": "grilled chicken salad",
                    "rating": 14
                },
                {
                    "data": "spaghetti bolognese",
                    "rating": 14
                },
                {
                    "data": "vegetable stir fry",
                    "rating": 14
                },
                {
                    "data": "cheeseburger",
                    "rating": 45
                },
                {
                    "data": "pepperoni pizza",
                    "rating": 88
                },
                {
                    "data": "fish tacos",
                    "rating": 35
                },
                {
                    "data": "beef burrito",
                    "rating": 75
                },
                {
                    "data": "chicken alfredo",
                    "rating": 65
                },
                {
                    "data": "lentil soup",
                    "rating": 25
                },
                {
                    "data": "bbq ribs",
                    "rating": 92
                },
                {
                    "data": "avocado toast",
                    "rating": 3
                },
                {
                    "data": "shrimp fried rice",
                    "rating": 55
                },
                {
                    "data": "pancake breakfast",
                    "rating": 77
                }
            ],

            
            "rules": "rating",
            "length": 10,
            # "compound_length": 3,
            # "compound_rules": "dfdfdf"
        }

        self.connector = Connector(data)

        self.connector.start_connect()

        self.connector.set_value("pancake breakfast", 1000)

        self.connector.alter_stream()
        self.connector.build_seed()


Demo()
import random
from main.core import MorphicSemanticEngine

import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

class Markov:


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.state = "Sunny"

        self.transition = {
                    "Sunny": {
                        "Sunny": .6,
                        "Rainy": .3,
                        "Cloudy": .1
                    },
                    "Rainy": {
                        "Sunny": .2,
                        "Rainy": .5,
                        "Cloudy": .3
                    },
                    "Cloudy": {
                        "Sunny": .3,
                        "Rainy": .3,
                        "Cloudy": .4
                    }
        }

        self.engine = None

        self.mse_tests = {
            "standard": self.mse_standard,
            "personal": self.mse_personal,
            "structured": self.mse_structured
        }

        self.step_count = 10

        self.run("standard")


    def run(self, test):
        print("\n\n\n\nMarkov Chain Output:\n")
        for step in range(self.step_count):
            print(step, self.state)
            self.state = self.next_state()
        print("\n\nMSE " + test.upper() + " Test")
        self.mse_tests[test]()


    def next_state(self):
        states = list(self.transition[self.state].keys())
        probs = list(self.transition[self.state].values())
        return random.choices(states, probs)[0]
    

    def define_mse(self):
        self.engine = MorphicSemanticEngine(
            [56, 46, 34, 185, 4355],
            ["Sunny", "Rainy", "Cloudy"]
        )


    def change_engine(self, params):
        self.engine.seed = params["seed"]
        self.engine.vocab = params["vocab"]
        self.engine.constants = params["constants"]
        self.engine.mod = params["mod"]


    def mse_standard(self):
        self.define_mse() if not self.engine else None
        self.engine.generate_tokens(self.step_count)

        

    def mse_personal(self):
        pass


    def mse_structured(self):
        pass

Markov()
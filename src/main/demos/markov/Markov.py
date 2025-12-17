import random
from core import MorphicSemanticEngine

import os
import sys



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

        self.tokens = None

        self.mse_tests = {
            "standard": self.mse_standard,
            "personal": self.mse_personal,
            "structured": self.mse_structured
        }

        self.test_count = 5
        self.step_count = 50

        


    def run(self, test):
        i = 1
        while i < self.test_count:
            print(f"\n\n\nTest #{i}")
            print("\n\nMarkov Chain Output:\n")
            for step in range(self.step_count):
                
                print(str(step+1) + " " + self.state)
                self.state = self.next_state()
            print("\n\nMSE " + test.upper() + " Test")
            self.mse_tests[test]()
            i+=1


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
        self.define_mse() 
        self.tokens = self.engine.generate_tokens(self.step_count) 
        self.print_tokens()

        # Markov generates values based on rating, with no memory. 
        # mse generates values based on seed output, with memory. always the same output given the same seed. if no particular order is needed, no need to test seed prior to setting the vocab. 


    def mse_personal(self):
        self.define_mse()

        vocab = []

        data = {
            "Sunny": random.randint(1, 100),
            "Rainy": random.randint(1, 100),
            "Cloudy": random.randint(1, 100), 
            "Foggy": random.randint(1, 100),
            "Heatwave": random.randint(1, 100),
            "Snow": random.randint(1, 100),
            "Hail": random.randint(1, 100),
            "Ice": random.randint(1, 100),
            "Lightning": random.randint(1, 100)
        }

        sorted= dict(sorted(data.items(), key=lambda x: x[1], reverse=True)) 

        print("\n\nsorted")
        print(sorted)


        # Markov generates values based on rating, with no memory. if only personalized values are used, the values are still generated randomly. there is no memory...no way to build the same chain every time.

        # mse generates values based on seed output, with memory. always the same output given the same seed. with personalization, only the highest rated values will be generated. if no particular order is needed, no need to test seed prior to setting the vocab. 


    def mse_structured(self):
        pass
        #markov is not able to build structure because there is no determinism.

        #if vocab is mapped with rules to mse output array values, structure is possible. shannons law is not violated due to the mapping rules plugin, but the seed can still be compressed to a minimal size.  


    def print_tokens(self):
        print()
        i = 1
        for token in self.tokens:
            print(f"{str(i)} {token}")
            i += 1
        print("\n\n")

Markov()
import random
from core import Stateshaper
from tests.Tests import Tests





class Markov:


    def __init__(self, **kwargs):
        

        self.tests = Tests()


        self.test_count = 1
        self.step_count = 50

        self.state = "Sunny"

        self.transition = self.markov_standard()

        self.engine = None

        self.tokens = None

        self.prev_state = None
        self.current_seed = None

        self.stateshaper_tests = {
            "standard": self.stateshaper_standard,
            "personal": self.stateshaper_personal
        }

        self.stateshaper_vocab = {
            "reversibility": self.stateshaper_reversibility,
            "deterministic": self.stateshaper_deterministic
        }

        self.markov_tests = {
            "standard": self.markov_standard,
            "personal": self.markov_personal
        }

    


    def run(self, test):
        self.transition = self.markov_tests[test]()
        self.state = list(self.transition.keys())[0]
        i = 0
        states = []
        while i < self.test_count:
            print(f"\nTest #{i+1}")
            print("\n\nMarkov Chain Output:\n")
            for step in range(self.step_count):
                print(str(step+1) + " " + self.state)
                states.append(self.state)
                self.prev_state = self.state
                self.state = self.next_state()
            i+=1
        return states
    

    def reverse(self, test):
        self.transition = self.markov_tests[test]()
        self.state = self.prev_state
        i = 0
        states = []
        while i < self.test_count:
            print(f"\nTest #{i+1}")
            print("\n\nMarkov Chain Output (Reverse Test):\n")
            for step in range(self.step_count):
                print("#" + str(step+1) + " " + self.state)
                states.append(self.state)
                self.prev_state = self.state
                self.state = self.next_state()
            i+=1
        return states


    def next_state(self):
        states = list(self.transition[self.state]["data"].keys())
        probs = list(self.transition[self.state]["data"].values())
        return random.choices(states, probs)[0]
    

    def define_stateshaper(self, test="reversibility"):
        self.engine = Stateshaper(
            [random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973)],
            self.stateshaper_vocab[test]()
    ) if test == "reversibility" else Stateshaper([111, 222, 456, 35, 76],
            self.stateshaper_vocab["deterministic"]())
        

    def stateshaper_reversibility(self):
        return ["Sunny", "Rainy", "Cloudy", "Hot", "Snow", "Freeze"]
    
    
    def stateshaper_deterministic(self):
        data = {
            "is starting to attack you!": random.randint(1, 100),
            "assumes a guarded position!": random.randint(1, 100),
            "is asking if you have anything to trade...": random.randint(1, 100),
            "runs and hides when they see you!": random.randint(1, 100),
            "asks if you want to join...": random.randint(1, 100),
            "is offering to help with your cause...": random.randint(1, 100),
            "wants to know where the nearest town is...": random.randint(1, 100),
            "is asking if you can repair their wagon...": random.randint(1, 100),
            "looks confused upon seeing you...": random.randint(1, 100),
        }

        sorted_items = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
 
        print("\n\nStateshaper deterministic values\n")
        print(sorted_items)

        return list(sorted_items.keys())[:3]


    def change_engine(self, params):
        self.engine.seed = params["seed"]
        self.engine.vocab = params["vocab"]
        self.engine.constants = params["constants"]
        self.engine.mod = params["mod"]


    def stateshaper_standard(self):
        self.tokens = self.engine.generate_tokens(self.step_count) 
        self.print_tokens()


    def stateshaper_personal(self):

        data = {
            "Sunny": 90,
            "Rainy": 76,
            "Cloudy": 56, 
            "Foggy": 89,
            "Heatwave": 45,
            "Snow": 67,
            "Hail": 87,
            "Ice": 43,
            "Lightning": 53
        }

        sorted_items = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
 
        print("\n\nStateshaper personalization values\n")
        print(sorted_items)

        return list(sorted_items.keys())[:3]


    def print_tokens(self):
        print()
        i = 1
        for token in self.tokens:
            print(f"{str(i)} {token}")
            i += 1
        print("\n\n")


    def markov_standard(self):
        return {
            "Sunny": {
                "data":{
                    "Sunny": .6,
                    "Rainy": .3,
                    "Cloudy": .1
                }
            },
            "Rainy": {
                "data":{
                    "Sunny": .2,
                    "Rainy": .5,
                    "Cloudy": .3
                }
            },
            "Cloudy": {
                "data":{
                    "Sunny": .3,
                    "Rainy": .3,
                    "Cloudy": .4
                }
            }
        }


    def markov_personal(self):
        data = {
            "is starting to attack you!": 
            {"rating": 67},
            "assumes a guarded position!": 
            {"rating": 83},
            "is asking if you have anything to trade...": 
            {"rating": 83},
            "runs and hides when they see you!": 
            {"rating": 23},
            "asks if you want to join...": 
            {"rating": 89},
            "is offering to help with your cause...": 
            {"rating": 53},
            "wants to know where the nearest town is...": 
            {"rating": 26},
            "is asking if you can repair their wagon...": 
            {"rating": 98},
            "looks confused upon seeing you...": 
            {"rating": 56},
        }

        sorted_items = dict(sorted(data.items(), key=lambda x: x[1]["rating"], reverse=True))
        rated_items = dict(list(sorted_items.items())[:3])
        for item in rated_items:
            rated_items[item]["data"] = {
                list(rated_items.keys())[0]: .6,
                list(rated_items.keys())[1]: .2,
                list(rated_items.keys())[2]: .2
            }
        return dict(list(sorted_items.items())[:3])
    

    def reverse_test(self, length, count, markov=True):
        self.define_stateshaper()
        self.step_count = length
        passed = 0 
        i = 0
        
        print("REVERSIBILITY TEST (MARKOV)\n" if markov == True else "\nREVERSIBILITY TEST (STATESHAPER)\n")
        while i < length:
            self.define_stateshaper()
            result = self.tests.reversibility({"compare": "markov", "forward": self.run, "reverse": self.reverse}, "standard") if markov == True else self.tests.reversibility({"compare": "stateshaper", "forward": self.engine.generate_tokens, "reverse": self.engine.reverse_tokens}, count)
            print(result)
            passed = passed + 1 if result == True else passed
            i += 1

        self.print.s(1)
        print(str(passed) + " Tests Passed out of " + str(length))
        


    def get_names(self):
        return random.choice(["Aelric", "Maya", "Thorin", "Jax", "Elowen", "Marcus", "Lyra", "Noah", "Kaelen", "Ava", "Rurik", "Lena", "Fenric", "Julian", "Seraphina", "Eli", "Vaelora", "Kai", "Corwin", "Mira", "Orwyn", "Talia", "Garron", "Zoe", "Sylphae", "Aelric Stone", "Maya Kepler", "Thorin Vale", "Jax Arlen", "Elowen Park", "Marcus Hale", "Lyra Ashcroft", "Noah Vance", "Kaelen Frost", "Ava Serris", "Rurik Mason", "Lena Ibarra", "Fenric Holt", "Julian Cross", "Seraphina Cole", "Eli Rowan", "Vaelora Quinn", "Kai Mercer", "Corwin Blake", "Mira Kade", "Orwyn Chen", "Talia Knox", "Garron Pierce", "Zoe Marin", "Sylphae Reed"])
    
    
    def deterministic_test(self, length, count, markov=True):
        self.define_stateshaper("deterministic")
        self.step_count = length
        passed = 0 
        i = 0
        name = self.get_names()
        
        print("DETERMINISTIC TEST (MARKOV)\n" if markov == True else "\nDETERMINISTIC TEST (STATESHAPER)\n")
        while i < length:
            self.define_stateshaper("deterministic")
            first_run = self.engine.generate_tokens(count)
            print(f"\n\n\nTest #{i+1}\n")
            print("\nInitial Test:\n")
            for action in first_run:
                print(name + " " + action)
            print("\n")
            self.engine.iteration = 1
            result = self.tests.determinism({"compare": "markov", "run": self.run}, "personal", self.run("personal")) if markov == True else self.tests.determinism({"compare": "stateshaper", "run": self.engine.generate_tokens}, count, first_run)
            print("\nNext Test:\n")
            for j in range(len(result[1])):
                print(name + " " + result[1][j])
            passed = passed + 1 if result[0] == True else passed
            print("\nMatch: " + str(result[0]))
            i += 1

        self.print.s(1)
        print(str(passed) + " Tests Passed out of " + str(length))
                


    def compression_test(self, length):
        self.tests.compression(length, "Markov")


Markov()
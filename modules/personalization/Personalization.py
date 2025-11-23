import os
import sys

# Find project root (two levels up from this file: modules/personalization/.. /..)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from modules.personalization.examples.Fitness import Fitness
from mse.core import MorphicSemanticEngine
from mse.classes.Modify import Modify


import random




class Personalization:

    def __init__(self, **kwargs):
        super(Personalization, self).__init__(**kwargs)


        self.selection = Fitness() #change based on type of selection
        self.modify = Modify()
        
        self.answers = ["A", "B", "C", "D"]
        self.questions()

        self.signature = self.create_signature()
        self.vocab = self.selection.get_vocab()

        if self.vocab == False:
            print("\n\nneeds more mapping rules")
            print(self.selection.ratings)
            print(self.selection.vocab)
            sys.exit()

        self.engine = MorphicSemanticEngine(
            initial_state=self.signature,
            vocab=self.vocab,
            constants={"a": 3, "b": 5, "c": 7, "d": 11},
            mod=9973,
        )

        self.original_tokens = self.last_tokens = self.engine.generate_tokens(50)

        self.new_tokens = None

        for i in range(1):
            self.modify.simulate_action(self.selection)

        self.modify.compare_actions(self.engine, self.original_tokens, self.new_tokens, self.last_tokens)



    def questions(self):
        i = 1 
        while i <= len(self.selection.questions.keys()):
            print("\n")
            print(self.selection.questions[i]["question"])
            print("\n")
            for answer in self.selection.questions[i]["choices"].keys():
                print(answer + ": " + self.selection.questions[i]["choices"][answer]["text"])
            print("\n")
            response = None
            while response not in self.answers:
                response = random.choice(self.answers)
            self.add_score(self.selection.questions[i]["choices"][response.upper()]["scores"])
            print("\n")
            i+=1

        print("\n\nend of questions")
        print("\n\n")

        
    def add_score(self, scores):
        for rating in self.selection.ratings.keys():
            self.selection.ratings[rating] += scores[rating]

        print("\n\nratings")
        print(self.selection.ratings)


    def create_signature(self, max_score=100):
        signature = []
        for key in self.selection.ratings.keys():
            val = int(round((self.selection.ratings[key] / max_score) * 9))
            val = max(0, min(9, val))
            signature.append(val)
        print("\n\nsignature")
        print(signature)
        return signature 
    

    # def simulate_action(self, selection):
    #     action = random.choice(list(self.selection.rules.items()))
    #     print("\n\ncurrent ratings")    
    #     print(self.selection.ratings)
    #     print("\nsimulated action")
    #     self.last_simulated = action[0]
    #     print(action[0])
    #     print("\naction ratings")
    #     print(action[1])

    #     for rating in list(self.selection.ratings.keys()):
    #         self.selection.ratings[rating] += action[1][rating]
    #     print("\nadjusted ratings")    
    #     print(self.selection.ratings)



Personalization()
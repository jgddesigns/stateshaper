from mse.core import MorphicSemanticEngine
from selections.Fitness import Fitness
import random

class Personalization:


     
    def __init__(self, **kwargs):
        super(Personalization, self).__init__(**kwargs)

        self.selection = Fitness() #change based on type of selection



        self.answers = ["A", "B", "C", "D"]
        self.questions()
        # self.signature = self.normalize()


        self.engine = MorphicSemanticEngine(
            initial_state=self.build_seed(self.normalize()),
            vocab=self.selection.get_vocab(),
            constants={"a": 3, "b": 5, "c": 7, "d": 11},
            mod=9973,
        )

        print("\n\ntokens")
        print(self.engine.generate_tokens(50))



    
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
                # response = input("Your Answer: ").upper()
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


    def normalize(self, max_score=100):
        signature = []
        for key in self.selection.ratings.keys():
            val = int(round((self.selection.ratings[key] / max_score) * 9))
            val = max(0, min(9, val))
            signature.append(val)
        print("\n\nsignature")
        print(signature)
        return signature 

        




Personalization()
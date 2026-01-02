


import sys


class CompressRatings:


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.vocab = None

        # test values
        self.master_ratings = {
            "a": 80,
            "b": 90, 
            "c": 10, 
            "d": 23,
            "e": 94, 
            "f": 45, 
            "g": 65,
            "h": 76, 
            "i": 82, 
            "j": 71
        }


        self.similarities = {
            "a": ["e", "b"],
            "b": ["a", "g", "h"],
            "c": ["d", "f", "h"],
            "d": ["a", "b", "j"],
            "e": ["c", "d"],
            "f": ["b", "c", "g"],
            "g": ["a", "b"],
            "h": ["c", "e", "h", "i"],
            "i": ["d", "e", "f"],
            "j": ["e"]   
        }


        self.input = [
            [True, ["c", "i"]],
            [True, ["a", "c", "i"]],
            [True, ["d", "e"]],
            [False, ["b", "g", "h"]],
            [True, ["a", "c", "f"]],
            [False, ["c", "d", "h", "i"]],
            [False, ["a", "b", "j"]],
            [True, ["d", "g", "h"]],
            [False, ["c", "e", "i"]],
            [True, ["h", "i"]],
        ]

        
        self.get_vocab(self.initial_ratings())
        print(self.vocab)
        self.derive_rankings()
        print(self.vocab)
        print(self.master_ratings)
        for _ in range(20):
            self.adjust_ratings(self.master_ratings)
            self.get_vocab(self.master_ratings)
            print(self.vocab)
            print(self.master_ratings)


    def initial_ratings(self, data=None, input=None):
        ratings = {}



        sort = sorted(data["input"], key=lambda x: list(x.values())[0]["rating"], reverse=True)

        print(sort)
        sys.exit()
        return [list(i.keys())[0] for i in sort]
    

        ratings = self.master_ratings
        return ratings
        

    def get_vocab(self, rankings, length=3):
        self.vocab = self.sort_ratings(rankings)[:length]
        

    def sort_ratings(self, ratings):
        return sorted(ratings, key=lambda x: ratings[x], reverse=True)
    
    
    def derive_rankings(self):
        ratings = {
            "a": 0,
            "b": 0, 
            "c": 0, 
            "d": 0,
            "e": 0, 
            "f": 0, 
            "g": 0,
            "h": 0, 
            "i": 0, 
            "j": 0
        }
        
        for item in self.vocab:
            ratings[item] += len(ratings) - self.vocab.index(item)
            [self.add_ratings(ratings, i, abs(self.vocab.index(item)-len(self.vocab))) for i in self.similarities[item]] 

        self.adjust_ratings(ratings)
        self.master_ratings = ratings
        self.get_vocab(ratings)

        return ratings
    

    def add_ratings(self, ratings, i, add):
        ratings[i] = ratings[i] + add


    def adjust_ratings(self, ratings):
        for item in self.input:
            [self.add_ratings(ratings, i, (1 if item[0] == True else -1)) for i in item[1]]

        


CompressRatings()
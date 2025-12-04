from random import randint

## used to define terms used in the mse.

## parameter format is dict/json with the following key/value pairs:

    # {
    #       "input": [],    ## list/array (the data to be called while the engine is running.)
    #       "rules": "",    ## string value (rating, compound, random or token. defines how the input will be mapped to the engine's vocab parameter.)          
    #       "length": None,  ## int (if none, uses all input.)
    #       "compound_length": None ## int (for combining compound vocab)
    #       "compound_rules": "random" string (further rules for compounding vocab. default is random.),
    # }
    

class Vocab:

    rule_types = None

    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)

        self.debug = True
        self.data = data if data else self.test_data()

        ## rating (personalization) - create a chain based on personalization derived from preference based 1-100 ratings 

        ## compound (synthetic data) - use a bank of terms and put them together based on the 'compound rules' parameter as the mse runs. uses 'compound_vocab' function in the mse 'tools' directory. 

        ## random (synthetic) - use a bank of defined terms to generate arbitrary output

        ## token (events, compression) - the vocab terms are used to call events in the program based on the data sequence 

        self.rule_types = ["random", "rating", "compound", "token"]

        self.mapping_types = {
            "random": self.random_mapping,
            "rating": self.rating_mapping,
            "compound": self.compound_mapping,
            "token": self.token_mapping 
        }

        self.current_rule = self.data["rules"] if self.valid_rule(self.data["rules"]) else self.rule_types[0]
        self.data_map = {}
        self.vocab = []

        print("\n\n")
        if isinstance(self.data, dict) == False:
            print("Data passed is in incorrect format. Please make sure it is a dict/json with keys 'input' (list) and 'rules' (string).")
            

        elif isinstance(self.data["input"], list) == False:
            print("The input list isn't formatted correctly. Please ensure it is formatted as a list/array.")
            

        elif self.data["rules"] and self.valid_rule(self.data["rules"]) == False:
            print("The rule chosen is not valid. Valid types are 'rating', 'compound', 'random', or 'token'.")
            
        
        elif self.data["rules"] == "rating" and self.valid_ratings() == False:
            print("The 'rating' rule has been chosen, but not all rules are defined. Please make sure each value in the input data set is in the following format:\n\n{'data': values here, 'rating': 0/100 rating here}.")
               
        
        elif self.data["length"] and isinstance(self.data["length"], int) == False:
            print("The length value is not an integer. Length will be set to input list size.")
            self.data["length"] = len(self.data["input"])
        
        else:
            print("\n\nData has been accepted. Processing input to enter into the MSE...")
            self.define() if not self.data["rules"]  and not self.debug else self.define(self.data["rules"]) if not self.debug else self.test()
        print("\n\n")

        
    def test_data(self):
        print("\n\nrunning test function.\n\n")
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
            
            "rules": "compound",
            "length": 10
        }


    def test(self):
        self.define(self.data["rules"])
        

    def valid_rule(self, rule):
        if rule not in self.rule_types:
            print("\nRule in data set is not in list of defined rules.")
        return rule in self.rule_types
    
    
    def valid_ratings(self):
        i = 0
        for item in self.data["input"]:
            i += 1
            if "data" not in item.keys() or "rating" not in item.keys() and len(item.keys()) == 2:
                print(f"Bad keys in object {i}.\n")
                return False
            if len(item.keys()) > 2:
                print(f"Too many keys in object {i}.\n")
                return False
            if isinstance(item["rating"], int) == True:
                if item["rating"] > 100 or item["rating"] < 0:
                    print(f"Rating is out of range in object {i}.\n")
                    return False
            if isinstance(item["rating"], int) == False:
                    print(f"Rating is not an integer in object {i}.\n")
                    return False
        print("Input 'rating' data is valid.\n")
        print("Length: " + str(self.data["length"]) + "\n")
        return True

 
    def valid_tokens(self):
        i = 0
        for item in self.data["input"]:
            if "data" not in item.keys() or "rank" not in item.keys()or "event" not in item.keys() and len(item.keys()) == 3:
                print(f"Bad keys in object {i}.\n")
                return False
            if len(item.keys()) > 3:
                print(f"Too many keys in object {i}.\n")
                return False
            if not item["rank"]:
                print(f"Rank value is not valid in object {i}.\n")
                return False
            if item["rank"] and isinstance(item["rank"], int) == False:
                print(f"Rank value is not an integer in object {i}.\n")
                return False
            if not item["event"]:
                print(f"Event value is not valid in object {i}.\n")
                return False
        print("Rule 'token' data is valid.\n")
        print("Length: " + str(self.data["length"]) + "\n")
        return True      


    def length_exists(self):
        if isinstance(self.data["length"], int):
            self.data["length"] = len(self.data["input"]) if self.data["length"] > len(self.data["input"]) else None

    
    def define(self, rules=None):
        if not rules:
            self.random_mapping() 
        else:
            self.mapping_method()

        
    def mapping_method(self):
        self.mapping_types[self.current_rule]()


    def random_mapping(self):
        self.vocab = self.data["input"]


    def rating_mapping(self):
        print("\n\nStarting ratings based mapping.\n")
        included = []

        input = self.sort_ratings()

        i = 0
        while len(included) < self.data["length"]:
            included.append(input[i]["data"])
            i+=1

        self.vocab = included

        print(f"\nMSE vocab parameter successfully set with 'rating' rule. Length: " + str(self.data["length"]))


    def sort_ratings(self):
        return sorted(self.data["input"], key=lambda x: x["rating"], reverse=True)
    

    def compound_mapping(self):
        self.vocab = "compound_mapping"
        self.compound_vocab = self.data["input"] if self.data["length"] == len(self.data["input"]) else self.compound_map()
        print(f"\nMSE vocab parameter successfully set with 'compound' rule. Length: " + str(self.data["length"]))


    def compound_map(self):
        included = []

        while len(included) < self.data["length"]:
            data = self.data["input"][randint(0, len(self.data["input"])-1)]
            included.append(data) if data not in included else None

        print(included)
        return included


    def token_mapping(self):

        pass


    def sort_token(self):
        return sorted(self.data["input"], key=lambda x: x["rank"], reverse=True)        


Vocab()
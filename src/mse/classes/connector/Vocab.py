from random import randint

## used to define_vocab terms used in the mse.

## data parameter format is dict/json with the following key/value pairs:

    # {
    #       "input": [],    ## list/array (the data to be called while the engine is running.)
    #       "rules": "",    ## string value (rating, compound, random or token. define_vocabs how the input will be mapped to the engine's vocab parameter.)          
    #       "length": None,  ## int (if none, uses all input.)
    #       "compound_length": None ## int (for combining compound vocab)
    #       "compound_rules": "random" string (further rules for compounding vocab. default is random. like groups can be specified for data to be generated),
    #       "compound_groups": groups included in the compound map. can be used along with compound_rules. by default only values within a group will be matched.,
    # }
    

class Vocab:


    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)

        self.rule_types = None
        self.debug = True
        self.data = data if data else self.test_data()

        self.rule_types = ["random", "rating", "compound", "token"]

        self.rules_explained = {
            "random": "The vocab consists of any terms within the input. If the length value is define_vocabd, the vocab list will include that many random values from the initial input data.",
            "rating": "Create the vocab based on 1-100 ratings. If the length value is define_vocabd, the vocab list will include that many items from the input data, based on the highest ratings. If no length is specified, the vocab will be all input.",
            "compound": "Items from the vocab list will be randomly combined based on the 'group' value and called during each iteration of the MSE engine. If a length is specified, the vocab list will be limited to that many items. If an compound_groups list is set, only those groups will be in the list, otherwise any group in the input data can be included.",
            "token": "The vocab list will consist of objects or functions that are called during MSE iterations. This will be based on a number ranking. If a length value is specified, the vocab list will be limited to that number. "
        }

        self.compound_rules = ["random"] ##need more compound rules. matching terms? rating based?

        self.mapping_types = {
            "random": self.random_mapping,
            "rating": self.rating_mapping,
            "compound": self.compound_mapping,
            "token": self.token_mapping 
        }

        self.current_rule = self.data["rules"] if self.valid_rule(self.data["rules"]) else self.rule_types[0]
        self.data_map = {}
        self.vocab = []


        

    def set_data(self, data):
        self.data = data
        self.valid_data()
        self.define_vocab(self.data["rules"])


    def valid_data(self):
        if self.data["rules"] and self.valid_rule(self.data["rules"]) == False:
            print("The rule chosen is not valid. Valid types are 'rating', 'compound', 'random', or 'token'. The rule will be defaulted to 'random'.")
            self.data["rules"] = "random"

        if (self.data["rules"] == "compound" and self.data["compound_length"] and isinstance(self.data["compound_length"], int) == False) or not self.data["compound_length"]:
            print("\n\nThe 'compound' rule has been chosen, but no compound length has been assigned. Using default compound length of 2.")
            self.data["compound_length"] = 2

        if (self.data["rules"] == "compound" and self.data["compound_rules"] and (isinstance(self.data["compound_rules"], int) == False or self.valid_compound_rules() == False)) or not self.data["compound_rules"]:
            print("\n\nThe 'compound' rule has been chosen, but no compound rules have been assigned, or the assigned rule is invalid. Using default compound rule'random'.")
            self.data["compound_rules"] = "random"

        if self.data["rules"] == "compound" and (self.data["compound_groups"] and  self.valid_compound_groups() == False) or not self.data["compound_groups"]:
            print("\n\nThe 'compound' rule has been chosen, but no compound rules have been assigned, or the assigned rule is invalid. Using default compound rule'random'.")
            self.data["compound_rules"] = "random"

        if self.data["length"] and isinstance(self.data["length"], int) == False:
            print("The length value is not an integer. Length will be set to input list size.")
            self.data["length"] = len(self.data["input"])

        print("\n\n")
        if isinstance(self.data, dict) == False:
            print("Data passed is in incorrect format. Please make sure it is a dict/json with keys 'input' (list) and 'rules' (string).")
            
        elif isinstance(self.data["input"], list) == False:
            print("The input list isn't formatted correctly. Please ensure it is formatted as a list/array.")
            
        elif self.data["rules"] == "random" and self.valid_random() == False:
            print("The 'random' rule has been chosen, but the input list is invalid. Please make sure each value in the input data set is in the following format:\n\n{'data': values here}.")

        elif self.data["rules"] == "rating" and self.valid_ratings() == False:
            print("The 'rating' rule has been chosen, but the input list is invalid. Please make sure each value in the input data set is in the following format:\n\n{'data': values here, 'rating': 0/100 rating here}.")

        elif self.data["rules"] == "compound" and self.valid_compound() == False:
            print("The 'compound' rule has been chosen, but the input list is invalid. Please make sure each value in the input data set is in the following format:\n\n{'data': values here, 'group': your specified group type, int or str}.")

        elif self.data["rules"] == "token" and self.valid_tokens() == False:
            print("The 'token' rule has been chosen, but not all rules are define_vocabd. Please make sure each value in the input data set is in the following format:\n\n{'data': use an object, function call etc to call base on the value in the mse array, 'rank': int in event calling order preference (1, 2, 3).")
      
        else:
            print("The data has been accepted. Processing input to enter into the MSE...")
            self.define_vocab() if not self.data["rules"]  and not self.debug else self.define_vocab(self.data["rules"]) if not self.debug else self.test()
        print("\n\n")


    def valid_rule(self, rule):
        if rule not in self.rule_types:
            print("\nRule in data set is not in list of define_vocabd rules.")
        return rule in self.rule_types
    

    def valid_map(self):
        ##combine all validity checks into one function
        pass

    
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
        print("Input 'rating' data is valid.\n\n")
        print("Length: " + str(self.data["length"]) + "\n\n")
        return True


    def valid_compound(self):
        i = 0
        for item in self.data["input"]:
            i += 1
            if "data" not in item.keys() or "group" not in item.keys() and len(item.keys()) == 2:
                print(f"Bad keys in object {i}.\n")
                return False
            if len(item.keys()) > 2:
                print(f"Too many keys in object {i}.\n")
                return False
            if (isinstance(item["group"], int) == False and isinstance(item["group"], str) == False):
                (f"Group is invalid in object {i}. Please make sure the group id is an int or str variable type.")
                return False
        print("Input 'compound' data is valid.\n\n")
        print("Length: " + str(self.data["length"]) + "\n\n")
        return True
    

    def valid_compound_rules(self):
        return self.data["compound_rules"] in self.compound_rules
    

    def valid_compound_groups(self):
        i = 0
        for item in self.data["input"]:
            i += 1
            if "group" not in item.keys() or not item["group"]:
                print(f"Compound rule is invalid in object {i}.\n")
                return False
        print("Compound groups are valid.\n\n")
        print("Length: " + str(self.data["length"]) + "\n\n")
        return True         
    
 
    def valid_tokens(self):
        i = 0
        for item in self.data["input"]:
            i += 1
            if "data" not in item.keys() or "rank" not in item.keys() and len(item.keys()) == 2:
                print(f"Bad keys in object {i}.\n")
                return False
            if len(item.keys()) > 2:
                print(f"Too many keys in object {i}.\n")
                return False
            if not item["rank"]:
                print(f"Rank value is not valid in object {i}.\n")
                return False
            if item["rank"] and isinstance(item["rank"], int) == False:
                print(f"Rank value is not an integer in object {i}.\n")
                return False
        print("Rule 'token' data is valid.\n\n")
        print("Length: " + str(self.data["length"]) + "\n\n")
        return True      


    def length_exists(self):
        if isinstance(self.data["length"], int):
            self.data["length"] = len(self.data["input"]) if self.data["length"] > len(self.data["input"]) else None

    
    def define_vocab(self):
        self.mapping_method()

        self.print_map()
        return self.vocab

        
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

        print(f"\nMSE vocab parameter successfully set with 'rating' rule.")


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

        return included


    def token_mapping(self):
        print("\n\nStarting token based mapping. Events will be called based on number ranking.\n")

        included = []
        input = self.sort_token()

        i = 0
        while len(included) < self.data["length"]:
            included.append(input[i]["data"])
            i+=1

        self.vocab = included

        print(f"\nMSE vocab parameter successfully set with 'token' rule. Length: " + str(self.data["length"]))


    def sort_token(self):
        return sorted(self.data["input"], key=lambda x: x["rank"], reverse=False)        


    def print_map(self):
        print("\n\nThe vocab list is set. Items:\n\n")

        for item in self.vocab:
            print(str(item))

        print(f"\n\nThe vocab will be called based on the '{str(self.current_rule)}' rule:\n")
        print(self.rules_explained[self.current_rule])


    def test(self):
        if not self.data["rules"]:
            self.data = self.test_data()
        self.define_vocab()


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


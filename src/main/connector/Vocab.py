# Used to define the vocab terms used in Stateshaper.

# Data parameter format is dict/json with the following key/value pairs:

# {
#       "input": [{"data": any, "rating": integer 1-100}],    ## list/array (the data to be called while the engine is running.)
#       "rules": "",    ## string value (rating, compound, random or token. define_vocabs how the input will be mapped to the engine's vocab parameter.)          
#       "length": None,  ## int (if none, uses all input.)
#       "compound_length": None ## int (for combining compound vocab)
#       "compound_rules": "random" string (further rules for compounding vocab. default is random. like groups can be specified for data to be generated),
#       "compound_groups": groups included in the compound map. can be used along with compound_rules. by default only values within a group will be matched.,
# }
    

class Vocab:


    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.rule_types = None
        self.debug = True
        self.data = data 

        try:
            self.random_mods = data["random_mods"]
        except:
            self.random_mods = [10, 7]

        try:
            self.random_constants = data["random_constants"]
        except:
            self.random_constants = [2, 3, 5, 8]

            

        self.rule_types = ["random", "rating", "compound", "token"]

        self.rules_explained = {
            "random": "The vocab consists of any terms within the input. If the length value is define_vocabd, the vocab list will include that many random values from the initial input data.",
            "rating": "Create the vocab based on 1-100 ratings. If the length value is define_vocabd, the vocab list will include that many items from the input data, based on the highest ratings. If no length is specified, the vocab will be all input.",
            "compound": "Items from the vocab list will be randomly combined based on the 'group' value and called during each iteration of Stateshaper engine. If a length is specified, the vocab list will be limited to that many items. If an compound_groups list is set, only those groups will be in the list, otherwise any group in the input data can be included.",

            # IN PROGRESS
            "token": "The vocab list will consist of objects or functions that are called during Stateshaper iterations. This will be based on a number ranking. If a length value is specified, the vocab list will be limited to that number. "
        }

        self.compound_rules = ["random"] 

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
            print("The 'token' rule has been chosen, but not all rules are define_vocabd. Please make sure each value in the input data set is in the following format:\n\n{'data': use an object, function call etc to call base on the value in the Stateshaper array, 'rank': int in event calling order preference (1, 2, 3).")
      
        else:
            print("The data has been accepted. Processing input to enter into Stateshaper...")
            self.define_vocab() if not self.data["rules"]  and not self.debug else self.define_vocab(self.data["rules"]) if not self.debug else self.test()

        print("\n\n")


    def valid_rule(self, rule):
        if rule not in self.rule_types:
            print("\nRule in data set is not in list of define_vocabd rules.")
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
        vocab = [i["data"] for i in self.data["input"] if self.data["input"].index(i) % (self.random_mods[0] if self.data["input"].index(i) % 2 == 0 else self.random_mods[1]) in self.random_constants]
        self.vocab = vocab


    def set_preferences(self, data, length=5):
        self.top_preferences = data[:length]


    def rating_mapping(self):
        print("\n\nStarting ratings based mapping.\n")
        personal = []
        export = []
        partial = []
        side = []
        full_list = []

        input = self.sort_ratings()

        self.set_preferences(input)

        i = 0
        for interest in self.data["input"]:        
            key = list(interest.keys())[0]
            for item in interest[list(interest.keys())[0]]["data"]:
                if len(export) < self.data["length"]:
                    if len([x for x in item["attributes"] if x in self.top_preferences and key == self.top_preferences[0]]) > 0:
                        export.append(item["item"])
                    elif len([x for x in item["attributes"] if x in self.top_preferences]) > 0 and len([y for y in self.top_preferences if key == y]) > 0:
                        partial.append(item["item"])
                    elif len([x for x in item["attributes"] if x in self.top_preferences]) > 0:
                        side.append(item["item"])
            i += 1


        full_list = export + partial + side
        while len(personal) < self.data["length"]:
            personal.append(full_list[len(personal)])

        print(f"\nStateshaper vocab parameter successfully set with 'rating' rule.\n")
        self.vocab = personal


    def sort_ratings(self, length=5):
        sort = sorted(self.data["input"], key=lambda x: list(x.values())[0]["rating"], reverse=True)
        return [list(i.keys())[0] for i in sort]
    

    def compound_mapping(self):
        if self.data["compound_groups"]:
            mandatory = [item[0] for item in self.data["compound_groups"] if item[1] == 1]
            groups = [group[0] for group in self.data["compound_groups"]]
            included = [item["data"] for item in self.data["input"] if any(x in item["groups"] for x in groups) and any(x in item["groups"] for x in mandatory)]
        else:
            included = [item["data"] for item in self.data["input"]]

        self.vocab = included

        print(f"\nStateshaper vocab parameter successfully set with 'compound' rule.")


    def token_mapping(self):
        print("\n\nStarting token based mapping. Events will be called based on number ranking.\n")

        included = []
        input = self.sort_token()

        i = 0
        while len(included) < self.data["length"]:
            included.append(input[i]["data"])
            i+=1

        self.vocab = included

        print(f"\nStateshaper vocab parameter successfully set with 'token' rule.")


    def sort_token(self):
        return sorted(self.data["input"], key=lambda x: x["rank"], reverse=False)        


    def print_map(self):
        print("\n\nThe vocab list is set. Items:\n\n")

        for item in self.vocab:
            print(str(item))

        print(f"\n\nThe vocab will be called based on the '{str(self.current_rule)}' rule:\n")
        print(self.rules_explained[self.current_rule])
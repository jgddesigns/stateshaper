

## used to define terms used in the mse.

## parameter format is dict/json with the following key/value pairs:

    # {
    #       "input": [] ## list/array,
    #       "rules": rating, compound, random or token ## string value
    # }


class Vocab:


    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

        if not isinstance(data, dict):
            print("Data passed is in incorrect format. Please make sure it is a dict/json with keys 'input' (list) and 'rules' (string).")
            return False

        elif not isinstance(data["input"], list):
            print("The term list isn't formatted correctly. Please ensure it is formatted as a list/array.")
            return False

        elif data["rules"] and not self.valid_rule(data["rules"]):
            print("The rule chosen is not valid. Valid types are 'rating', 'compound', 'random', or 'token'.")
            return False
        
        else:
            self.define(data["input"]) if not data["rules"] else self.define(data["input"], data["rules"]) 


        ## rating (personalization) - create a chain based on personalization derived from preference based 1-10 ratings 

        ## compound (synthetic data) - use a bank of terms and put them together. 

        ## random (syntheic) - use a bank of defined terms to generate without meaning

        ## token (compression) - the vocab terms are used to call events in the program based on the data sequence 
        self.rule_types = ["rating", "compound", "random", "token"]


        self.constraints = False
        self.current_rule = "random"
        self.data_map = {}
        self.vocab = []
        


    ## define whether a data stream is random or has contraints. if so, what are the constraints based on? 
    def define(self, input, rules=None):
        if not rules:
            self.vocab = input["terms"] 
        
        else:
            self.set_rules()

        

    def set_rules(self):
        pass



    def set_current_rule(self, rule):
        pass


    def valid_rule(self, rule):
        return rule in self.rule_types
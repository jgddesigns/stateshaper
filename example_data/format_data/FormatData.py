import sys


class FormatData:

    def __init__(self, input=None, **kwargs):
        super().__init__(**kwargs)

        self.parent_terms = {
            "rating": ["input", "rules", "length"],
            "compound": ["input", "rules", "length", "compound_length", "compound_groups", "compound_terms"],
            "random": ["input", "rules", "length"]
        }

        self.row_terms = {
            "rating": ["rating", "data"],
            "compound": ["data", "groups"],
            "random": ["data"]
        }

        self.data_types = {
            "input": [],
            "rules": "",
            "length": 0,
            "compound_length": 0,
            "compound_groups": [],
            "compound_terms": []
        }

        self.compound_group = ["", 0]

        self.current_template = input

        self.add_rows = {
            "compound": self.compound_row,
            "random": self.random_row,
            "rating": self.rating_row
        }

        self.rating_example()

        



    
    def data_template(self, rule, length):
        data = {} 

        for term in self.parent_terms[rule]:
            data[term] = None

        for key in list(data.keys()):
            data[key] = self.data_types[key]

        data["rules"] = rule
        data["length"] = length

        return data


    def row_template(self, rule):
        row_data = {
            "rating": {"rating": 0, "data": {}}, 
            "compound": {"data": "", "groups": []},
            "random": {"data": ""}
        }

        row = {}

        for item in self.row_terms[rule]:
            row[item] = None

        for item in list(row.keys()):
            row[item] = row_data[rule][item]
        
        return row
    

    def build_template(self, rule, length=3):
        self.current_template = self.data_template(rule, length)

    
    def add_row(self, rule, item, attributes=None, key=None):
        row = self.add_rows[rule](item, attributes, key)
        place = str(len(self.current_template["input"])+1)
        print(f"\nCreated row #{place} for current '{rule}' rule template.")
        self.current_template["input"].append(row)
        return True

    def remove_row(self, item, rule, key=None):
        if rule == "rating":
            rows = [i for i in self.current_template["input"] if (list(i.items())[0][0] == key)]
        else:
            rows = [i for i in self.current_template["input"] if (list(i.items())[0][1] == item) or (isinstance(item, object) and item in str(object))]

        for row in rows:
            place = str(self.current_template["input"].index(row)+1)
            print(f"\nRemoved row #{place} in current '{rule}' rule template.")
            self.current_template["input"].pop(self.current_template["input"].index(row))


    def add_group(self, group, include):
        self.current_template["compound_groups"].append([group, include]) 


    def remove_group(self, group):
        groups = [i for i in group if i[0] == group]

        for item in groups:
            self.current_template["compound_groups"].pop(self.current_template["compound_groups"].index(item))


    def add_term(self, term):
        self.current_template["compound_terms"].append(term)


    def remove_term(self, term):
        self.current_template["compound_terms"].pop(self.current_template["compound_terms"].index(term))


    def add_compound_length(self, length):
        self.current_template["compound_length"] = length


    def rating_row(self, item, attributes, key):
        row = {}

        row[key] = self.row_template("rating")
        row[key]["data"]["item"] = item
        row[key]["data"]["attributes"] = attributes

        return row
    

    def add_rating(self, key, rating):
        row = [i for i in self.current_template["input"] if list(i.keys())[0] == key][0]
        print(row)
        list(row.items())[0][1]["rating"] = rating


    def random_row(self, item, attributes=None, key=None):
        row = self.row_template("random")
        row["data"] = item

        return row


    def compound_row(self, item, groups, key=None):
        row = self.row_template("compound")
        row["data"] = item
        row["groups"] = groups

        return row


    def get_data(self):
        return self.current_template


    def compound_example(self):
        self.build_template("compound", 5)
        self.add_row("compound", "chocolate", ["candy", "cake", "pie", "chocolate"])
        self.add_row("compound", "lemon", ["candy", "pie", "fruit", "juice"])
        self.add_row("compound", "orange", ["candy", "fruit", "juice"])
        self.add_group("candy", 1)
        self.add_group("chocolate", 0)
        self.add_group("pie", 0)       
        self.add_term("and")        
        self.add_compound_length(3) 
        print("\n\nhere is the created template:\n")
        print(self.current_template)


    def random_example(self):
        self.build_template("random", 4) 
        self.add_row("random", "macaroni and cheese")
        self.add_row("random", "chicken pot pie")
        self.add_row("random", "frozen yogurt")
        print("\n\nhere is the created template:\n")
        print(self.current_template)


    def rating_example(self):
        self.build_template("rating", 5)
        self.add_row("rating", "baseball.png", ["baseball", "basketball", "football"], "sports")
        self.add_row("rating", "boggle.png", ["scrabble", "jenga"], "puzzle")
        self.add_row("rating", "wow.png", ["final fantasy", "fallout", "overwatch"], "mmorpg")
        self.add_rating("sports", 75)
        self.add_rating("puzzle", 53)
        self.add_rating("mmorpg", 95)
        print("\n\nhere is the created template:\n")
        print(self.current_template)

    
FormatData()
import sys


class ParseInput:

    def __init__(self, input=None, **kwargs):
        super().__init__(**kwargs)

        self.parent_terms = {
            "derived": ["input", "rules", "length"],
            "compound": ["input", "rules", "length", "compound_length", "compound_groups", "compound_terms"],
            "random": ["input", "rules", "length"]
        }

        self.row_terms = {
            "derived": ["rating", "data"],
            "compound": ["data", "groups"],
            "random": ["data"]
        }

        self.row_data = {
            "derived": {"rating": 0, "data": {"item": "", "attributes": []}}, 
            "compound": {"data": "", "groups": []},
            "random": {"data": ""}
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



        # self.data_template("random")
        # self.row_template("random")
        print(self.derived_row("test item", 'self.data_template("derived")', ["attr1", "attr2", "attr3"]))



    def data_template(self, rule):
        data = {} 

        for term in self.parent_terms[rule]:
            data[term] = None

        for key in list(data.keys()):
            data[key] = self.data_types[key]

        return data


    def row_template(self, rule):
        row = {}

        for item in self.row_terms[rule]:
            row[item] = None

        for item in list(row.keys()):
            row[item] = self.row_data[rule][item]

        return row
    

    def build_template(self, rule):
        pass


    def derived_row(self, key, item, attributes):
        row = {}

        row[key] = self.row_template("derived")

        row[key]["data"]["item"] = item
        row[key]["data"]["attributes"] = attributes

        return row


    def random_row(self, item):
        row = self.row_template("random")
        row["data"] = item

        return row


    def compound_row(self, item, groups):
        row = self.row_template("compound")
        row["data"] = item
        row["groups"] = groups

        return row

    
ParseInput()
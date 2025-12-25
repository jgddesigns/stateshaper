import sys


class Modify:


    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.edit = None
        self.result = None
        self.data = data

        # self.get_keys()


    def get_keys(self):
        items = [list(i.items()) for i in self.data["input"]]

        print(items)
        # dict(i[1]
        sys.exit()

        data = [[str(i[0][1]), i[1][1]] for i in items] if self.data["rules"] != "random" else [[str(i[0][1])] for i in items]

        edit = {} 

        for item in data:
            edit[item[0]] = item[1] if self.data["rules"] != "random" else item[0]

        self.edit = edit


    def modify(self, key, rating):
        self.edit[key] = rating


    def adjust(self, key, adjust):
        self.edit[key] += adjust


    def export(self):
        result = [] 
        
        for item in self.edit:
            result.append({"data": item, "rating": self.edit[item]})

        self.result = result
        return result
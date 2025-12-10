

class InfiniSet:

    def __init__(self, array, constants={"a": 5, "b": 7, "c": 9, "d": 11}, mod=55, **kwargs):
        super().__init__(**kwargs)

        self.array = array
        self.constants = constants
        self.mod = mod
        self.events = None

        self.array_size = len(self.array)

        self.test()




    def test(self):
        self.events = {
            5:  "A",
            10: "B",
            15: "C",
            20: "D",
            25: "E",
            30: "F",
            35: "G",
            40: "H",
            45: "I",
            50: "J",
        }

        
        self.map([5, 10, 15, 20, 25])
        i = 0
        while i < 100:
            self.morph()
            self.logic()
            i+=1


    def map(self, data):
        self.array = data


    def morph(self):
        self.map([(i*2) % self.mod for i in self.array])


    def logic(self):
        print()
        for value in self.array:
            print(self.events[value])



InfiniSet([5, 10, 15, 20, 25])
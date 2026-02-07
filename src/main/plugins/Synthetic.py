import random


class Synthetic:


    def __init__(self, token=1, **kwargs):

        self.default_constants = 3
        self.constants = {}




    def create_value(self, token):
        pass


    def get_constants(self, length, increment=2, random=False):
        constants = []
        start = 3
        
        for _ in range(length):
            increment = random.randint(1, 99) if random == True else increment
            constants.append(start)
            start = start + increment

        return constants


    def create_constants(self, numbers=None, length=None, increment=2, random=False):
        length = self.default_constants if not length else length
        numbers = self.get_constants(length=length, increment=increment, random=random) if not numbers else numbers
        start = 97
        for number in numbers:
            self.constants[chr(start)] = number
            start += 1

        print("\nconstants")
        print(self.constants)


Synthetic()
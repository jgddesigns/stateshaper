import random


import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)



class MappingRules:



    def __init__(self, **kwargs):
        super(MappingRules, self).__init__(**kwargs)
        

        self.user_id = self.get_id()

        self.demographic = self.get_demographic()

        self.preferences = self.get_preferences()
        



    def get_id(self, key=None):
        return 1234
    

    def get_demographic(self, random=None):
        demographic = {
            "age": 73, 
            "gender": 0,
            "household_income": 88000,
            "education_level": 3,
            "household_status": 2,
            "employment_status": 4,
            "home_ownership": 1,
            "media_consumption_level": 38,
            "device_usage": 81
        }

        return demographic if not random else self.random_demographic()


    def random_demographic(self):
        return {
            "age": random.randint(18, 80),
            "gender": random.randint(0, 2),
            "household_income": random.randint(20000, 200000),
            "education_level": random.randint(0, 3),
            "household_status": random.randint(0, 3),
            "employment_status": random.randint(0, 4),
            "home_ownership": random.randint(0, 1),
            "media_consumption_level": random.randint(1, 100),
            "device_usage": random.randint(1, 100)
        }


    def get_preferences(self, random=None):
        interests = {
            "reading": 57,
            "traveling": 12,
            "cooking": 88,
            "hiking": 41,
            "photography": 63,
            "music": 95,
            "gaming": 29,
            "fitness": 77,
            "gardening": 14,
            "painting": 68,
            "writing": 53,
            "coding": 92,
            "movies": 36,
            "sports": 81,
            "diy_projects": 47,
            "knitting": 9,
            "biking": 72,
            "swimming": 25,
            "yoga": 84,
            "dancing": 33
        }


        return interests if random == None else self.random_interests()

        ## in real version
        ## get interests based on user id
        return self.adjust_interests(interests)
    

    def adjust_interests(self):
        pass


    ## DEMO ONLY
    def random_interests(self):
        interests = {
            "reading": random.randint(1, 100),
            "traveling": random.randint(1, 100),
            "cooking": random.randint(1, 100),
            "hiking": random.randint(1, 100),
            "photography": random.randint(1, 100),
            "music": random.randint(1, 100),
            "gaming": random.randint(1, 100),
            "fitness": random.randint(1, 100),
            "gardening": random.randint(1, 100),
            "painting": random.randint(1, 100),
            "writing": random.randint(1, 100),
            "coding": random.randint(1, 100),
            "movies": random.randint(1, 100),
            "sports": random.randint(1, 100),
            "diy_projects": random.randint(1, 100),
            "knitting": random.randint(1, 100),
            "biking": random.randint(1, 100),
            "swimming": random.randint(1, 100),
            "yoga": random.randint(1, 100),
            "dancing": random.randint(1, 100)
        }

        return interests



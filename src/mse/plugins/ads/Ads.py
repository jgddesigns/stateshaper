import random
from ad_list import ad_list

class Ads:




    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.user_id = user_id
        self.interests = None
        self.top_interests = None

        self.data_format = {
            "input": [],
            "rules": "rating",
            "length": 10
        }

        if user_id:
            print("\nFetching user based on entered user ID.")
            self.get_user()
        else:
            print("\nCreating new user.")
            self.create_user()


    ## get user seed from database.
    def get_user(self):

        ## for demo use mock seed. 
        self.current_seed = {
            "user_id": "1234",
            "state": [
                3404,
                832,
                2194,
                6734,
                105
            ],
            "vocab": [],
            "mod": 9973,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }
        }


    def create_user(self):
        self.user_id = "1235"
        self.create_data()


    def create_seed(self):
        self.current_seed = {
            "user_id": self.user_id,
            "state": [
                3404,
                832,
                2194,
                6734,
                105
            ],
            "vocab": [],
            "mod": 9973,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }
        }


    def create_data(self, random=None):
        pass


    def get_interests(self, randomize=None):
        self.interests = {
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
         } if not randomize else self.random_interests()


    def random_interests(self):
        return {
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
    

    def adjust_interests(self):
        pass


    def set_interests(self, length=3):
        self.top_interests = sorted(self.interests, key=lambda x: x, reverse=True)[:length]


    # build a list of the ads to be shown. contains actual url. for demo, some images will be included in this directory.
    def get_ads(self):
        ads = []

        for item in ad_list.items():
            included = [i for i in item if self.matching_interests() > 1]


import random
from plugins.ads.ad_list import ad_list
from random import randint




class Ads:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.user_id = user_id
        self.interests = None
        self.top_interests = ["reading", "traveling", "cooking"]
        self.most_relevant = 0

        self.data_format = {
            "input": None,
            "rules": "rating",
            "length": 10
        }

        # self.test()

        # if user_id:
        #     print("\nFetching user based on entered user ID.")
        #     self.get_user()
        # else:
        #     print("\nCreating new user.")
        #     self.create_user()


    def test(self):
        print("running test\n\n")
        # print(self.get_ads())
        self.random_interests()
        print(self.interests)
        print()
        self.set_interests()
        return self.get_ads()
        print()

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
        self.interests = {
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
        self.top_interests = sorted(self.interests, key=lambda x: self.interests[x], reverse=True)[:length]

        print(self.top_interests)


    # build a list of the ads to be shown. contains actual url. for demo, some images will be included in this directory.
    def get_ads(self, ad_count=10):
        ads = [] 
        side = []

        for interest in ad_list.items():         
            for item in interest[1]:
                if len(ads) < ad_count:
                    ads.append(item["link"]) if len([x for x in item["attributes"] if x in self.top_interests and interest[0] == self.top_interests[0]]) > 0 else side.append(item["link"])
                    self.most_relevant = self.most_relevant + 1 if len([x for x in item["attributes"] if x in self.top_interests and interest[0] == self.top_interests[0]]) > 0 else self.most_relevant

        print(f"\n\n{self.most_relevant} highly relevant ads\n")

        while len(ads) < ad_count:
            ads.append(side[randint(0, len(side)-1)]) if len(side) > 0 else None

        print("\nselected ads")
        print(ads)
        
        return ads



    def define_data(self):
        pass



# Ads()
import random

from src.main.tools.tiny_mse.TinyMSE import TinyMSE

from .ad_list import ad_list
from random import randint
import hashlib
import random
import string
import os
import sys



PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)






class Ads:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.tiny_mse = TinyMSE(5)

        self.seed_store = {}
        self.seed = ""
        self.compressed_vocab = ""
        self.subseed_length = 2
        self.decoded_subset = 0
        self.relevant = 0

        self.user_id = user_id
        self.interests = None
        self.ads = None
        self.top_interests = ["reading", "traveling", "cooking"]
        self.most_relevant = 0

        self.data_format = {
            "input": None,
            "rules": "rating",
            "length": 10
        }


    def change_data(self, data):
        self.interests = data
        self.set_interests()
        return self.get_ads()


    def get_data(self):
        self.random_interests()
        self.set_interests()
        return self.get_ads()
    

    def get_user(self):

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
            "travel": 12,
            "cooking": 88,
            "fitness": 77,
            "writing": 53,
            "science": 92,
            "movies": 36,
            "sports": 81,
            "history": 56,
            "crafts": 34,
            "animals": 63

         } if not randomize else self.random_interests()


    def random_interests(self):
        self.interests = {
            "travel": random.randint(1, 100),
            "cooking": random.randint(1, 100),
            "fitness": random.randint(1, 100),
            "writing": random.randint(1, 100),
            "science": random.randint(1, 100),
            "movies": random.randint(1, 100),
            "sports": random.randint(1, 100),
            "history": random.randint(1, 100),
            "crafts": random.randint(1, 100),
            "animals": random.randint(1, 100),
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

        print("\n\nMSE TARGETED AD DEMO\n\nThis demonstration shows how app related storage data can be reduced by over 80%.\n\n")
        print("\n\nRandom interest list has been generated. The highest rated interests are:\n")
        print(self.top_interests)


    # build a list of the ads to be shown. contains actual url. for demo, some images will be included in this directory.
    def get_ads(self):
        ads = [] 
        side = []
        seed = ""
        relevant = ""
        side_seed = ""

        for interest in ad_list.items():         
            for item in interest[1]:
                if len(ads) < self.tiny_mse.list_count:
                    idx1 = list(ad_list.keys()).index(interest[0])
                    idx2 = interest[1].index(item)

                    seed = seed + f"{idx1:02d}{idx2:02d}"
                    if len([x for x in item["attributes"] if x in self.top_interests and interest[0] == self.top_interests[0]]) > 0:
                        ads.append(item["link"])
                        self.most_relevant = self.most_relevant + 1
                        relevant = relevant + f"{idx1:02d}{idx2:02d}"
                    else:
                        side.append(item["link"])
                        side_seed = side_seed + f"{idx1:02d}{idx2:02d}"

        print(f"\n\n\n{self.most_relevant} highly relevant ads have been added to the ad list:\n")

        print(ads)

        self.seed = relevant = relevant + side_seed[:self.tiny_mse.subset_size-len(relevant)]

        self.compressed_vocab = self.tiny_mse.compress(seed)

        self.subset_seed = self.tiny_mse.encode_subset_seed(seed, relevant)

        self.decoded_subset = self.tiny_mse.decode_subset_seed(seed, self.subset_seed)

        i = 0
        while len(ads) < self.tiny_mse.list_count:
            ads.append(side[i]) if len(side) > 0 else None
            i+=1

        print("\n\n\nFull ad list based on ratings profile:\n")
        print(ads)

        print("\n\n\nCompressed Tiny MSE format for entire ad list:\n")
        print(self.compressed_vocab)

        print("\n\n\nCompressed seed for chosen ad set:\n")
        print(self.subset_seed)

        print("\n\n\nAd list rebuilt from extracted seed:\n")
        print(self.rebuild_ads())
        print("\n\n")
        
        return ads
    

    def rebuild_ads(self):
        ads = []
        while len(ads)<self.tiny_mse.list_count:
            parent = self.decoded_subset[:2]
            child = self.decoded_subset[2:4]
            ads.append(ad_list[list(ad_list.keys())[int(parent)]][int(child)]["link"])
            self.decoded_subset = self.decoded_subset[4:]
        return ads
from random import randint
from modules.advertising.classes.AdLinks import AdLinks
from modules.advertising.classes.MappingRules import MappingRules
from mse.core import MorphicSemanticEngine

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)




class Advertising:

    ad_count = 10

    def __init__(self, **kwargs):
        super(Advertising, self).__init__(**kwargs)

        self.most_relevant = 0

        self.original_tokens = None

        self.engine = None

        self.mapping_rules = MappingRules()

        self.ad_links = AdLinks()

        self.preferences = self.set_preferences()

        self.ad_list = self.set_list()

        self.vocab = self.set_vocab()

        self.start_engine()

        




    def set_preferences(self):
        return sorted(self.mapping_rules.preferences, key=self.mapping_rules.preferences.get, reverse=True)[:5] if self.mapping_rules.preferences else None


    def set_list(self):
        ads = []
        for interest in self.preferences:
            ads.append(self.ad_links.links[interest])
        return ads


    def set_vocab(self):
        vocab = [] 
        side = []

        for interest in self.ad_list:            
            for item in interest:
                vocab.append(item["link"]) if len([x for x in item["attributes"] if x in self.preferences]) > 0 else side.append(item["link"])
                self.most_relevant = self.most_relevant + 1 if len([x for x in item["attributes"] if x in self.preferences]) > 0 else self.most_relevant

        while len(vocab) < self.ad_count:
            vocab.append(side[randint(0, len(side)-1)]) if len(side) > 0 else None

        return vocab


    def start_engine(self):
        self.engine = MorphicSemanticEngine(
            initial_state=self.get_state(),
            vocab=self.vocab,
            constants={"a": 3, "b": 5, "c": 7, "d": 11},
            mod=9973,
        )

        self.original_tokens = self.engine.generate_tokens(50)

        print("\n\n")
        print(self.original_tokens)
        

    def get_state(self):
        return [55, 346, 43, 115, 82]
    

Advertising()
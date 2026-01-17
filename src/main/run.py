import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

sys.path.append(os.path.dirname(__file__))

from classes.connector.Connector import Connector
from demos.lesson_plan.LessonPlan import LessonPlan
from core import Stateshaper




class RunEngine:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin = LessonPlan()
        self.connector = Connector(self.plugin.sort_ratings())

        self.engine = None

        self.seed = None
        self.compressed_seed = None
        self.run_engine()


    def run_engine(self):
        self.seed = self.connector.start_connect()

        self.engine = Stateshaper(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"]
        )

        self.tokens = self.engine.generate_tokens(self.connector.token_count)
        
        print("\n\nTokens successfully generated from vocab.\n")

        print(self.tokens)

        print()
    
    def compress_seed(self):
        self.seed["vocab"] = [self.plugin.compressed_vocab, self.plugin.compressed_subset]



# RunEngine()
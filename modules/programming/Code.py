import os
import sys
import random


HERE = os.path.dirname(__file__)

SRC_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)



from dataclasses import dataclass
from typing import Callable, List, Tuple
from modules.programming.examples.python.quiz.Quiz import Quiz
from mse.core import MorphicSemanticEngine



### uses mse token stream to create code from seed array. seed array is based on mapping rules. mse logic builds and runs the code. code doesnt need to be stored. rules entered to mse once, then runs on token stream. 
class Code:


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.session = Quiz()

        self.test()


    def test(self):
        self.generate_code(1)
        self.run_code(1)



    # return data to create seed
    def generate_code(self, seed: List[int], count: int = 10) -> Tuple[List[str], List[bool]]:
        return self.session.function_map["generate_seed"]() 
    
 

    #runs the code created from the seed
    def run_code(self, seed: List[int] | None = None, count: int = 10) -> None:
        self.session.function_map["run_code"]()



    # rules to create the seed. for code it is predetermined
    def get_tokens(self, ratings=None):
        return None


Code()

from demos.fintech_qa.FintechQA import FintechQA

import sys
from core import Stateshaper 
from example_data.format_data.FormatData import FormatData
# from tools.compress_json.CompressJson import CompressJson
from stateshaper import RunEngine
import json

class Demo:


    def __init__(self, input=None, **kwargs):
        


        self.qa_test()


    def qa_test(self):
        with open("example_data/tokens.json", "r") as f:
            data = json.loads(f.read())

        f.close()

        # seed = {'s': [66, 67, 54, 3, 34], 'v': ['AAA05101', '23589CHIJM'], 'c': {'a': 3, 'b': 5, 'c': 7, 'd': 11}, 'm': 9973}
        # self.engine = RunEngine(data, seed=seed, token_count=50)
        self.engine = RunEngine(data, token_count=50)
        self.engine.start_engine()
        self.engine.run_engine()



    def json_test(self):
        self.compress = CompressJson()

        self.compress.compress(self.test_json(1))


    def test_json(n: int):
        return {
            1: {
                "a": 1, "b": 1, "c": 1, "d": 1, "e": 1
            },
            2: {
                "user": "jay",
                "role": "user",
                "status": "active",
                "profile": {
                    "user": "jay",
                    "role": "user",
                    "status": "active"
                }
            },
            3: {
                "level1": {
                    "level2": {
                        "level3": {
                            "level4": {
                                "value": 42,
                                "flag": True
                            }
                        }
                    }
                }
            },
            4: {
                "big_number": 1234567890123456789012345678901234567890,
                "bigger_number": 9999999999999999999999999999999999999999
            },
            5: {
                "data": [
                    {"x": 1, "y": 2},
                    {"x": 1, "y": 2},
                    {"x": 1, "y": 2},
                    {"x": 1, "y": 2}
                ]
            },
            6: {
                "id": 837462,
                "name": "compression_test",
                "enabled": True,
                "threshold": 0.0003125,
                "tags": ["alpha", "beta", "gamma"],
                "meta": None
            },
            7: {
                "payload": "xA9fQ2LzP0wE7RkM4S1H3VJdC6yN5bT8uGm"
            },
            8: {
                "text1": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "text2": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "text3": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            },
            9: {
                "a": None, "b": None, "c": None, "d": None, "e": None
            },
            10: {
                "window": {
                    "width": 1920,
                    "height": 1080,
                    "fullscreen": False
                },
                "audio": {
                    "volume": 0.75,
                    "mute": False
                },
                "controls": {
                    "jump": "space",
                    "fire": "mouse1",
                    "reload": "r"
                }
            },
            11: {
                "this_is_a_very_long_key_name_used_for_testing_compression": 1,
                "this_is_a_very_long_key_name_used_for_testing_compression_2": 2,
                "this_is_a_very_long_key_name_used_for_testing_compression_3": 3
            },
            12: {
                "sequence": [1, 2, 3, 4, 5] * 3
            }
        }.get(n)


    def test1(self):
        with open("example_data/compound.json", "r") as f:
            data = json.loads(f.read())

        f.close()

        # seed = {'s': [66, 67, 54, 3, 34], 'v': ['AAA05101', '23589CHIJM'], 'c': {'a': 3, 'b': 5, 'c': 7, 'd': 11}, 'm': 9973}
        # self.engine = RunEngine(data, seed=seed, token_count=50)
        self.engine = RunEngine(data, token_count=50)
        self.engine.start_engine()
        self.engine.run_engine()
        self.engine.jump(1000)
        self.engine.jump(1000)
        self.engine.jump(1000)

    
    def test2(self):
        with open("example_data/rating_initial.json", "r") as f:
            data = json.loads(f.read())

        f.close()

        self.engine = RunEngine(data, token_count=50)
        self.engine.start_engine()
        self.engine.run_engine()
        seed = self.engine.get_seed(True)



        with open("example_data/rating_derived.json", "r") as f:
            data = json.loads(f.read())

        f.close()

        self.engine = RunEngine(data, seed=seed, token_count=50)

        self.engine.start_engine()
        self.engine.run_engine()
        self.engine.adjust_ratings()
        self.engine.run_engine()

        seed = self.engine.get_derived()



        with open("example_data/rating_derived.json", "r") as f:
            data = json.loads(f.read())

        f.close()

        self.engine = RunEngine(data, seed=seed, token_count=50)


        self.engine.start_engine()
        self.engine.run_engine()
        
        self.engine.adjust_ratings()
        self.engine.rebuild()
        print(self.engine.engine.iteration)
        self.engine.run_engine()

        print(self.engine.get_derived())
Demo()
import random
from tests.ca.CellularAutomata import CellularAutomata
from tests.markov.Markov import Markov
from connector.Connector import Connector
from tools.tiny_state.TinyState import TinyState


class Demo:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        # self.automata = CellularAutomata()

        # self.automata.run(.47, 7)

        # self.markov = Markov()
        # self.markov_test()
        # self.connector = None

        # self.tiny_state = TinyState()
        # self.tiny_state.get_seed(self.test_data())

        # self.connector_test(self.compound_test())



    def markov_test(self):
        self.markov.reverse_test(50, 10, False)
        self.markov.reverse_test(50, 10)
        self.markov.deterministic_test(10, 10, False)
        self.markov.deterministic_test(10, 10)
        self.markov.compression_test(100)
        self.markov.compression_test(50)
        self.markov.compression_test(25)
        self.markov.compression_test(10)


    def connector_test(self, data):
        
        self.connector = Connector(data)

        self.connector.start_connect()

        # self.connector.set_value("pancake breakfast", 1000)

        # self.connector.alter_stream()
        # self.connector.build_seed()



    def test_data(self):
        # return {
        #     "team": {
        #         "rating": 55,
        #         "events": [
        #             {"item": "football.png", "attributes": ["team", "contact", "outdoor"]},
        #             {"item": "basketball.png", "attributes": ["team", "indoor", "fast-paced"]},
        #             {"item": "soccer.png", "attributes": ["team", "endurance", "outdoor"]}
        #         ]
        #     },

        #     "individual": {
        #         "rating": 97,
        #         "events": [
        #             {"item": "tennis.png", "attributes": ["individual", "court", "precision"]},
        #             {"item": "golf.png", "attributes": ["individual", "outdoor", "precision"]},
        #             {"item": "climbing.png", "attributes": ["individual", "strength", "indoor"]}
        #         ]
        #     },

        #     "combat": {
        #         "rating": 71,
        #         "events": [
        #             {"item": "boxing.png", "attributes": ["combat", "individual", "indoor"]},
        #             {"item": "mma.png", "attributes": ["combat", "discipline", "individual"]},
        #             {"item": "wrestling.png", "attributes": ["combat", "grappling", "mat"]}
        #         ]
        #     },

        #     "water": {
        #         "rating": 88,
        #         "events": [
        #             {"item": "swimming.png", "attributes": ["water", "endurance", "individual"]},
        #             {"item": "surfing.png", "attributes": ["water", "balance", "outdoor"]},
        #             {"item": "waterpolo.png", "attributes": ["water", "team", "endurance"]}
        #         ]
        #     },

        #     "cycling": {
        #         "rating": 66,
        #         "events": [
        #             {"item": "cycling.png", "attributes": ["cycling", "endurance", "outdoor"]},
        #             {"item": "mountain_biking.png", "attributes": ["cycling", "terrain", "outdoor"]},
        #             {"item": "bmx.png", "attributes": ["cycling", "stunts", "individual"]}
        #         ]
        #     },

        #     "track": {
        #         "rating": 59,
        #         "events": [
        #             {"item": "sprinting.png", "attributes": ["track", "speed", "individual"]},
        #             {"item": "marathon.png", "attributes": ["track", "endurance", "road"]},
        #             {"item": "relay.png", "attributes": ["track", "team", "speed"]}
        #         ]
        #     },

        #     "winter": {
        #         "rating": 66,
        #         "events": [
        #             {"item": "skiing.png", "attributes": ["winter", "outdoor", "individual"]},
        #             {"item": "snowboarding.png", "attributes": ["winter", "balance", "outdoor"]},
        #             {"item": "biathlon.png", "attributes": ["winter", "endurance", "precision"]}
        #         ]
        #     },

        #     "recreation": {
        #         "rating": 42,
        #         "events": [
        #             {"item": "skateboarding.png", "attributes": ["recreation", "balance", "stunts"]},
        #             {"item": "surfskate.png", "attributes": ["recreation", "outdoor", "balance"]},
        #             {"item": "parkour.png", "attributes": ["recreation", "agility", "urban"]}
        #         ]
        #     },

        #     "precision": {
        #         "rating": 50,
        #         "events": [
        #             {"item": "archery.png", "attributes": ["precision", "focus", "individual"]},
        #             {"item": "shooting.png", "attributes": ["precision", "control", "individual"]},
        #             {"item": "golf_putting.png", "attributes": ["precision", "technique", "individual"]}
        #         ]
        #     },

        #     "digital": {
        #         "rating": 88,
        #         "events": [
        #             {"item": "esports.png", "attributes": ["digital", "competitive", "team"]},
        #             {"item": "sim_racing.png", "attributes": ["digital", "precision", "individual"]},
        #             {"item": "virtual_chess.png", "attributes": ["digital", "strategy", "mental"]}
        #         ]
        #     }
        # }

        return {
            "strength": {
                "rating": 78,
                "events": [
                    {"item": "powerlifting.png", "attributes": ["strength", "barbell", "individual"]},
                    {"item": "strongman.png", "attributes": ["strength", "carry", "outdoor"]},
                    {"item": "weightlifting.png", "attributes": ["strength", "olympic", "precision"]}
                ]
            },

            "endurance": {
                "rating": 82,
                "events": [
                    {"item": "ultramarathon.png", "attributes": ["endurance", "distance", "road"]},
                    {"item": "cycling_stage.png", "attributes": ["endurance", "cycling", "outdoor"]},
                    {"item": "rowing.png", "attributes": ["endurance", "water", "team"]}
                ]
            },

            "speed": {
                "rating": 74,
                "events": [
                    {"item": "100m.png", "attributes": ["speed", "track", "individual"]},
                    {"item": "drag_racing.png", "attributes": ["speed", "motor", "reaction"]},
                    {"item": "speed_skating.png", "attributes": ["speed", "ice", "individual"]}
                ]
            },

            "agility": {
                "rating": 69,
                "events": [
                    {"item": "parkour.png", "attributes": ["agility", "urban", "movement"]},
                    {"item": "gymnastics.png", "attributes": ["agility", "balance", "precision"]},
                    {"item": "fencing.png", "attributes": ["agility", "combat", "reaction"]}
                ]
            },

            "balance": {
                "rating": 63,
                "events": [
                    {"item": "slackline.png", "attributes": ["balance", "control", "outdoor"]},
                    {"item": "surfing.png", "attributes": ["balance", "water", "outdoor"]},
                    {"item": "paddleboard.png", "attributes": ["balance", "water", "endurance"]}
                ]
            },

            "coordination": {
                "rating": 66,
                "events": [
                    {"item": "table_tennis.png", "attributes": ["coordination", "reaction", "indoor"]},
                    {"item": "badminton.png", "attributes": ["coordination", "speed", "court"]},
                    {"item": "juggling.png", "attributes": ["coordination", "skill", "practice"]}
                ]
            },

            "reaction": {
                "rating": 71,
                "events": [
                    {"item": "goalkeeping.png", "attributes": ["reaction", "team", "reflex"]},
                    {"item": "esports_fps.png", "attributes": ["reaction", "digital", "precision"]},
                    {"item": "boxing_mitts.png", "attributes": ["reaction", "combat", "training"]}
                ]
            },

            "precision": {
                "rating": 85,
                "events": [
                    {"item": "archery.png", "attributes": ["precision", "focus", "individual"]},
                    {"item": "darts.png", "attributes": ["precision", "aim", "indoor"]},
                    {"item": "rifle.png", "attributes": ["precision", "control", "range"]}
                ]
            },

            "strategy": {
                "rating": 88,
                "events": [
                    {"item": "chess.png", "attributes": ["strategy", "mental", "individual"]},
                    {"item": "go.png", "attributes": ["strategy", "territory", "mental"]},
                    {"item": "poker.png", "attributes": ["strategy", "probability", "competition"]}
                ]
            },

            "teamwork": {
                "rating": 76,
                "events": [
                    {"item": "basketball.png", "attributes": ["teamwork", "court", "fast-paced"]},
                    {"item": "volleyball.png", "attributes": ["teamwork", "coordination", "court"]},
                    {"item": "rowing_team.png", "attributes": ["teamwork", "endurance", "water"]}
                ]
            },

            "leadership": {
                "rating": 70,
                "events": [
                    {"item": "quarterback.png", "attributes": ["leadership", "team", "decision"]},
                    {"item": "captaincy.png", "attributes": ["leadership", "strategy", "communication"]},
                    {"item": "coach_sim.png", "attributes": ["leadership", "planning", "analysis"]}
                ]
            },

            "focus": {
                "rating": 83,
                "events": [
                    {"item": "meditative_archery.png", "attributes": ["focus", "precision", "calm"]},
                    {"item": "snooker.png", "attributes": ["focus", "aim", "indoor"]},
                    {"item": "free_throw.png", "attributes": ["focus", "routine", "control"]}
                ]
            },

            "power": {
                "rating": 79,
                "events": [
                    {"item": "shot_put.png", "attributes": ["power", "throw", "track"]},
                    {"item": "hammer_throw.png", "attributes": ["power", "rotation", "track"]},
                    {"item": "sledge_training.png", "attributes": ["power", "conditioning", "outdoor"]}
                ]
            },

            "flexibility": {
                "rating": 61,
                "events": [
                    {"item": "yoga.png", "attributes": ["flexibility", "balance", "control"]},
                    {"item": "martial_forms.png", "attributes": ["flexibility", "flow", "discipline"]},
                    {"item": "stretching.png", "attributes": ["flexibility", "recovery", "practice"]}
                ]
            },

            "stamina": {
                "rating": 77,
                "events": [
                    {"item": "boxing_rounds.png", "attributes": ["stamina", "combat", "endurance"]},
                    {"item": "crossfit.png", "attributes": ["stamina", "conditioning", "mixed"]},
                    {"item": "soccer_match.png", "attributes": ["stamina", "team", "field"]}
                ]
            },

            "control": {
                "rating": 72,
                "events": [
                    {"item": "gym_rings.png", "attributes": ["control", "strength", "gymnastics"]},
                    {"item": "balance_beam.png", "attributes": ["control", "balance", "precision"]},
                    {"item": "freestyle_ski.png", "attributes": ["control", "air", "winter"]}
                ]
            },

            "timing": {
                "rating": 68,
                "events": [
                    {"item": "baseball_hitting.png", "attributes": ["timing", "bat", "reaction"]},
                    {"item": "cricket_batting.png", "attributes": ["timing", "precision", "field"]},
                    {"item": "jump_rope.png", "attributes": ["timing", "coordination", "rhythm"]}
                ]
            },

            "rhythm": {
                "rating": 64,
                "events": [
                    {"item": "speed_bag.png", "attributes": ["rhythm", "boxing", "coordination"]},
                    {"item": "rowing_stroke.png", "attributes": ["rhythm", "team", "water"]},
                    {"item": "aerobics.png", "attributes": ["rhythm", "endurance", "movement"]}
                ]
            },

            "conditioning": {
                "rating": 75,
                "events": [
                    {"item": "interval_training.png", "attributes": ["conditioning", "intensity", "fitness"]},
                    {"item": "hill_sprints.png", "attributes": ["conditioning", "power", "outdoor"]},
                    {"item": "sled_push.png", "attributes": ["conditioning", "strength", "drive"]}
                ]
            },

            "mobility": {
                "rating": 60,
                "events": [
                    {"item": "joint_flow.png", "attributes": ["mobility", "control", "health"]},
                    {"item": "animal_moves.png", "attributes": ["mobility", "agility", "ground"]},
                    {"item": "dynamic_warmup.png", "attributes": ["mobility", "prep", "routine"]}
                ]
            },

        }


    def compound_test(self):
        return {
            "input": [
                {
                    "data": "sausage",
                    "groups": ["meat", "breakfast"]
                },
                {
                    "data": "salad",
                    "groups": ["vegetable", "lunch", "dinner"]
                },
                {
                    "data": "pizza",
                    "groups": ["italian", "lunch", "dinner"]
                },
                {
                    "data": "pancakes",
                    "groups": ["breakfast", "sweet"]
                },
                {
                    "data": "bacon",
                    "groups": ["meat", "breakfast"]
                },
                {
                    "data": "eggs",
                    "groups": ["breakfast", "protein"]
                },
                {
                    "data": "burger",
                    "groups": ["meat", "lunch", "dinner"]
                },
                {
                    "data": "tacos",
                    "groups": ["mexican", "lunch", "dinner"]
                },
                {
                    "data": "sandwich",
                    "groups": ["lunch", "fast"]
                },
                {
                    "data": "soup",
                    "groups": ["dinner", "comfort"]
                },
                {
                    "data": "steak",
                    "groups": ["meat", "dinner", "breakfast"]
                },
                {
                    "data": "chicken",
                    "groups": ["protein", "lunch", "dinner"]
                },
                {
                    "data": "fish",
                    "groups": ["seafood", "dinner"]
                },
                {
                    "data": "pasta",
                    "groups": ["italian", "dinner"]
                },
                {
                    "data": "rice",
                    "groups": ["grain", "side"]
                },
                {
                    "data": "fries",
                    "groups": ["side", "fast"]
                },
                {
                    "data": "oatmeal",
                    "groups": ["breakfast", "grain"]
                },
                {
                    "data": "yogurt",
                    "groups": ["breakfast", "dairy"]
                },
                {
                    "data": "fruit bowl",
                    "groups": ["fruit", "breakfast"]
                },
                {
                    "data": "ice cream",
                    "groups": ["dessert", "sweet"]
                },
                {
                    "data": "cookies",
                    "groups": ["dessert", "sweet"]
                },
                {
                    "data": "cake",
                    "groups": ["dessert", "sweet"]
                },
                {
                    "data": "smoothie",
                    "groups": ["drink", "healthy"]
                },
                {
                    "data": "wrap",
                    "groups": ["lunch", "fast"]
                },
                {
                    "data": "cereal",
                    "groups": ["breakfast", "grain"]
                }
            ],

            "rules": "random",
            "length": 100,
            # "compound_length": 3,
            # "compound_groups": [["breakfast", 1], ["meat", 0]],
            # "compound_groups": [["breakfast", 1]],
            # "compound_terms": ["and", "with"]
        }

    def vocab_test(self):
        return [i["data"] for i in self.compound_test()["input"] if self.compound_test()["input"].index(i) % random.randint(2, 5) == 0]
    

Demo()
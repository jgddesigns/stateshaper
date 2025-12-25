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


    def random_test(self):
        return {
            "input": [
                { "data": "rain" },
                { "data": "snow" },
                { "data": "hail" },
                { "data": "sleet" },
                { "data": "fog" },
                { "data": "mist" },
                { "data": "thunderstorm" },
                { "data": "lightning" },
                { "data": "tornado" },
                { "data": "hurricane" },
                { "data": "cyclone" },
                { "data": "typhoon" },
                { "data": "drizzle" },
                { "data": "heat wave" },
                { "data": "cold front" },
                { "data": "warm front" },
                { "data": "blizzard" },
                { "data": "dust storm" },
                { "data": "sandstorm" },
                { "data": "monsoon" },
                { "data": "rainbow" },
                { "data": "frost" },
                { "data": "dew" },
                { "data": "overcast" },
                { "data": "clear skies" }
            ],
            "rules": "random",
            "length": 100
        }



    def rating_test(self):
        return {
            "input": [
                {"strength_training": {"rating": 78, "data": [{"item": "kettlebell_lift.png", "attributes": ["strength_training","power_exercise","conditioning_workout"]}]}},
                {"endurance_run": {"rating": 82, "data": [{"item": "trail_run.png", "attributes": ["endurance_run","stamina_build","marathon_training"]}]}},
                {"sprint_speed": {"rating": 74, "data": [{"item": "sprint_track.png", "attributes": ["sprint_speed","timing_practice","agility_course"]}]}},
                {"agility_course": {"rating": 69, "data": [{"item": "obstacle_course.png", "attributes": ["agility_course","coordination_drill","mobility_drill"]}]}},
                {"balance_challenge": {"rating": 63, "data": [{"item": "tightrope.png", "attributes": ["balance_challenge","control_drill","flexibility_session"]}]}},
                {"coordination_drill": {"rating": 66, "data": [{"item": "drumming.png", "attributes": ["coordination_drill","rhythm_training","timing_practice"]}]}},
                {"reaction_test": {"rating": 71, "data": [{"item": "ping_pong.png", "attributes": ["reaction_test","coordination_drill","focus_practice"]}]}},
                {"precision_training": {"rating": 85, "data": [{"item": "sniper_training.png", "attributes": ["precision_training","focus_practice","strategy_game"]}]}},
                {"strategy_game": {"rating": 88, "data": [{"item": "war_sim.png", "attributes": ["strategy_game","precision_training","teamwork_drill"]}]}},
                {"teamwork_drill": {"rating": 76, "data": [{"item": "relay_race.png", "attributes": ["teamwork_drill","stamina_build","leadership_task"]}]}},
                {"leadership_task": {"rating": 70, "data": [{"item": "team_coaching.png", "attributes": ["leadership_task","teamwork_drill","strategy_game"]}]}},
                {"focus_practice": {"rating": 83, "data": [{"item": "meditation.png", "attributes": ["focus_practice","precision_training","reaction_test"]}]}},
                {"power_exercise": {"rating": 79, "data": [{"item": "clap_pushup.png", "attributes": ["power_exercise","strength_training","conditioning_workout"]}]}},
                {"flexibility_session": {"rating": 61, "data": [{"item": "contortion.png", "attributes": ["flexibility_session","balance_challenge","mobility_drill"]}]}},
                {"stamina_build": {"rating": 77, "data": [{"item": "rowing.png", "attributes": ["stamina_build","endurance_run","conditioning_workout"]}]}},
                {"control_drill": {"rating": 72, "data": [{"item": "hoverboard.png", "attributes": ["control_drill","balance_challenge","flexibility_session"]}]}},
                {"timing_practice": {"rating": 68, "data": [{"item": "drum_circle.png", "attributes": ["timing_practice","sprint_speed","coordination_drill"]}]}},
                {"rhythm_training": {"rating": 64, "data": [{"item": "dance_routine.png", "attributes": ["rhythm_training","coordination_drill","focus_practice"]}]}},
                {"conditioning_workout": {"rating": 75, "data": [{"item": "crossfit_box.png", "attributes": ["conditioning_workout","power_exercise","stamina_build"]}]}},
                {"mobility_drill": {"rating": 60, "data": [{"item": "foam_rolling.png", "attributes": ["mobility_drill","agility_course","flexibility_session"]}]}},
                {"deadlift_session": {"rating": 81, "data": [{"item": "deadlift.png", "attributes": ["deadlift_session","strength_training","power_exercise"]}]}},
                {"marathon_training": {"rating": 84, "data": [{"item": "marathon.png", "attributes": ["marathon_training","endurance_run","stamina_build"]}]}},
                {"hurdle_run": {"rating": 73, "data": [{"item": "hurdles.png", "attributes": ["hurdle_run","agility_course","sprint_speed"]}]}},
                {"soccer_drill": {"rating": 72, "data": [{"item": "soccer_dribble.png", "attributes": ["soccer_drill","teamwork_drill","stamina_build"]}]}},
                {"surfing_practice": {"rating": 65, "data": [{"item": "surf_board.png", "attributes": ["surfing_practice","balance_challenge","mobility_drill"]}]}},
                {"volleyball_training": {"rating": 67, "data": [{"item": "volleyball_spike.png", "attributes": ["volleyball_training","teamwork_drill","coordination_drill"]}]}},
                {"boxing_reaction": {"rating": 70, "data": [{"item": "boxing_reaction.png", "attributes": ["boxing_reaction","reaction_test","stamina_build"]}]}},
                {"dart_practice": {"rating": 84, "data": [{"item": "dart_throw.png", "attributes": ["dart_practice","precision_training","focus_practice"]}]}},
                {"board_strategy": {"rating": 87, "data": [{"item": "board_game.png", "attributes": ["board_strategy","strategy_game","precision_training"]}]}},
                {"soccer_teamwork": {"rating": 75, "data": [{"item": "soccer_game.png", "attributes": ["soccer_teamwork","teamwork_drill","leadership_task"]}]}},
                {"orchestra_lead": {"rating": 71, "data": [{"item": "orchestra_conductor.png", "attributes": ["orchestra_lead","leadership_task","focus_practice"]}]}},
                {"archery_focus": {"rating": 82, "data": [{"item": "archery_target.png", "attributes": ["archery_focus","precision_training","focus_practice"]}]}},
                {"vertical_jump": {"rating": 80, "data": [{"item": "vertical_jump.png", "attributes": ["vertical_jump","power_exercise","strength_training"]}]}},
                {"pilates_session": {"rating": 60, "data": [{"item": "pilates.png", "attributes": ["pilates_session","flexibility_session","mobility_drill"]}]}},
                {"tennis_endurance": {"rating": 76, "data": [{"item": "tennis_match.png", "attributes": ["tennis_endurance","stamina_build","coordination_drill"]}]}},
                {"skateboard_control": {"rating": 71, "data": [{"item": "skateboard_trick.png", "attributes": ["skateboard_control","control_drill","agility_course"]}]}},
                {"boxing_timing": {"rating": 67, "data": [{"item": "boxing_combo.png", "attributes": ["boxing_timing","timing_practice","reaction_test"]}]}},
                {"jump_rope_rhythm": {"rating": 63, "data": [{"item": "jump_rope_routine.png", "attributes": ["jump_rope_rhythm","rhythm_training","coordination_drill"]}]}},
                {"stair_conditioning": {"rating": 74, "data": [{"item": "stair_climb.png", "attributes": ["stair_conditioning","conditioning_workout","stamina_build"]}]}},
                {"hip_mobility": {"rating": 59, "data": [{"item": "hip_mobility.png", "attributes": ["hip_mobility","mobility_drill","flexibility_session"]}]}},
                {"bench_press": {"rating": 79, "data": [{"item": "bench_press.png", "attributes": ["bench_press","strength_training","power_exercise"]}]}},
                {"swimming_marathon": {"rating": 83, "data": [{"item": "swimming_lap.png", "attributes": ["swimming_marathon","endurance_run","stamina_build"]}]}},
                {"bike_sprint": {"rating": 75, "data": [{"item": "bike_sprint.png", "attributes": ["bike_sprint","sprint_speed","timing_practice"]}]}},
                {"basketball_drill": {"rating": 70, "data": [{"item": "basketball_dribble.png", "attributes": ["basketball_drill","coordination_drill","teamwork_drill"]}]}},
                {"snowboard_balance": {"rating": 64, "data": [{"item": "snowboard.png", "attributes": ["snowboard_balance","balance_challenge","control_drill"]}]}},
                {"cycling_marathon": {"rating": 79, "data": [{"item": "cycling_marathon.png", "attributes": ["cycling_marathon","endurance_run","stamina_build"]}]}},
                {"acrobatics_control": {"rating": 74, "data": [{"item": "acrobatics.png", "attributes": ["acrobatics_control","agility_course","control_drill"]}]}},
                {"soccer_tackle": {"rating": 70, "data": [{"item": "soccer_tackle.png", "attributes": ["soccer_tackle","soccer_drill","coordination_drill"]}]}},
                {"rowing_rhythm": {"rating": 66, "data": [{"item": "rowing_stroke.png", "attributes": ["rowing_rhythm","rhythm_training","stamina_build"]}]}},
                {"boxing_training": {"rating": 78, "data": [{"item": "boxing_training.png", "attributes": ["boxing_training","stamina_build","conditioning_workout"]}]}},
                {"quarterback_drill": {"rating": 70, "data": [{"item": "quarterback_drill.png", "attributes": ["quarterback_drill","leadership_task","teamwork_drill"]}]}}],
            "rules": "rating",
            "length": 5
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

            "rules": "compound",
            "length": 100,
            "compound_length": 3,
            "compound_groups": [["breakfast", 1], ["meat", 0]],
            "compound_groups": [["breakfast", 1]],
            "compound_terms": ["and", "with"]
        }

    def vocab_test(self):
        return [i["data"] for i in self.compound_test()["input"] if self.compound_test()["input"].index(i) % random.randint(2, 5) == 0]
    

Demo()
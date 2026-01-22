import random
import sys


class DeriveVocab:


    def __init__(self, **kwargs):
        self.vocab = None

        self.original_data = None

        self.master_rankings = None

        self.derived_rankings = None

        self.similarities = None

        self.input_ranking = 3




    def initial_rankings(self, data=None):
        data = self.original_data = data if data else self.test_data()
        rankings = {}
        similarities = {}

        for item in data["input"]:
            rankings[list(item.keys())[0]] = list(item.values())[0]["rating"]
            try:
                similarities[list(item.keys())[0]] = list(item.values())[0]["data"]["attributes"]
            except:
                similarities[list(item.keys())[0]] = list(item.values())[0]["data"][0]["attributes"]

        self.master_rankings = rankings
        self.similarities = similarities
        self.get_vocab(rankings)
        self.derive_rankings()

        return self.vocab
        

    def get_vocab(self, rankings, length=None, data=None):
        self.vocab = self.sort_rankings(rankings)[:self.original_data["length"] if not length else length]
        return self.vocab
        

    def current_vocab(self):
        try:
            vocab = [list(i.values())[0]["data"][0]["item"] for i in self.original_data["input"] if [j for j in self.vocab if j == list(i.keys())[0]]]
        except:
            vocab = [list(i.values())[0]["data"]["item"] for i in self.original_data["input"] if [j for j in self.vocab if j == list(i.keys())[0]]]
        return vocab
    

    def sort_ratings(self, rankings):
        data = {}
        sort = sorted(rankings, key=lambda x: rankings[x], reverse=True)
        for item in sort:
            data[item] = rankings[item]
        return data
    

    def sort_rankings(self, rankings):
        rankings = sorted(rankings, key=lambda x: rankings[x], reverse=True)
        return rankings
    

    def derive_rankings(self):
        rankings = self.master_rankings

        for item in self.vocab:
            rankings[item] += len(rankings) - self.vocab.index(item)
            [self.add_rankings(rankings, i, abs(self.vocab.index(item)-len(self.vocab))) for i in self.similarities[item]] 

        self.master_rankings = rankings
        return rankings
    

    def post_derived(self):
        for item in self.original_data["input"]:
            item[list(item.keys())[0]]["rating"] += round(sum([self.master_rankings[i] for i in item[list(item.keys())[0]]["data"]["attributes"]])/len(item[list(item.keys())[0]]["data"]["attributes"]))
        self.sort_data(self.original_data)
        for item in self.original_data["input"]:
            item[list(item.keys())[0]].pop("rating", None)

        return self.original_data
    

    def get_master(self):
        return self.original_data
    

    def sort_data(self, data):
        sort = sorted(data["input"], key=lambda x: list(x.values())[0]["rating"], reverse=True)
        return sort
    

    def add_rankings(self, rankings, i, add):
        try:
            rankings[i] = rankings[i] + add
        except:
            pass


    def create_dataset(self, input, data):
        rankings = {}
        for item in data["input"]:
            rankings[list(item.keys())[0]] = 0

        for item in input:
            adjust = [list(i.keys())[0] for i in data["input"] if self.shared_attributes(item, i[list(i.keys())[0]]["data"]["attributes"]) == True]
            rankings = self.fill_rankings(rankings, adjust, item, input[item])

        rankings = self.sort_ratings(rankings)
        return rankings


    def fill_rankings(self, rankings, adjust, item, value):
        rankings[item] += 1
        for fill in adjust:
            try:
                rankings[fill] += 1
            except:
                pass
        for rank in rankings:
            try:
                if rank in adjust:
                    rankings[rank] = rankings[rank] + 1 if value == True else rankings[rank] - 1
            except:
                pass
        rankings.pop(item, None) if value == None else None
        return rankings


    def shared_attributes(self, input, data):
        item = list([i for i in self.original_data["input"] if list(i.keys())[0] == input][0].items())[0][1]["data"]["attributes"]
        return len([i for i in item if i in data]) > 0 

   
    def adjust_rankings(self, input, data=None):
        self.original_data = data if data else self.original_data
        rankings = self.create_dataset(input, data)
        self.master_rankings = rankings
        return self.get_vocab(rankings)
    

    # the original dataset (rating_initial.json in example data folder). it is what will actually be outputted by the core engine. this can be any type of data, but needs to be in this format. the actual values being used in the output are in the 'data'->'item' key of each item. the attributes are intended to be used for all similar items and can be used to adjust the vocab after the initial list has been built. for the vocab output, items with the top ratings will be chosen and the size is based on the value of the length key in the dataset.
    def test_data(self):
        return {
            "input": [
                {"strength_training": {"rating": 85, "data": {"item": "kettlebell_lift.png", "attributes": ["power_exercise","conditioning_workout"]}}},
                {"endurance_run": {"rating": 74, "data": {"item": "trail_run.png", "attributes": ["stamina_build","marathon_training"]}}},
                {"sprint_speed": {"rating": 72, "data": {"item": "sprint_track.png", "attributes": ["timing_practice","agility_course"]}}},
                {"agility_course": {"rating": 70, "data": {"item": "obstacle_course.png", "attributes": ["coordination_drill","mobility_drill"]}}},
                {"balance_challenge": {"rating": 66, "data": {"item": "tightrope.png", "attributes": ["control_drill","flexibility_session"]}}},
                {"coordination_drill": {"rating": 69, "data": {"item": "drumming.png", "attributes": ["rhythm_training","timing_practice"]}}},
                {"reaction_test": {"rating": 72, "data": {"item": "ping_pong.png", "attributes": ["coordination_drill","focus_practice"]}}},
                {"precision_training": {"rating": 76, "data": {"item": "sniper_training.png", "attributes": ["focus_practice","strategy_game"]}}},
                {"strategy_game": {"rating": 69, "data": {"item": "war_sim.png", "attributes": ["precision_training","teamwork_drill"]}}},
                {"teamwork_drill": {"rating": 72, "data": {"item": "relay_race.png", "attributes": ["stamina_build","leadership_task"]}}},
                {"leadership_task": {"rating": 71, "data": {"item": "team_coaching.png", "attributes": ["teamwork_drill","strategy_game"]}}},
                {"focus_practice": {"rating": 78, "data": {"item": "meditation.png", "attributes": ["precision_training","reaction_test"]}}},
                {"power_exercise": {"rating": 86, "data": {"item": "clap_pushup.png", "attributes": ["strength_training","conditioning_workout"]}}},
                {"flexibility_session": {"rating": 63, "data": {"item": "contortion.png", "attributes": ["balance_challenge","mobility_drill"]}}},
                {"stamina_build": {"rating": 73, "data": {"item": "rowing.png", "attributes": ["endurance_run","conditioning_workout"]}}},
                {"control_drill": {"rating": 71, "data": {"item": "hoverboard.png", "attributes": ["balance_challenge","flexibility_session"]}}},
                {"timing_practice": {"rating": 70, "data": {"item": "drum_circle.png", "attributes": ["sprint_speed","coordination_drill"]}}},
                {"rhythm_training": {"rating": 68, "data": {"item": "dance_routine.png", "attributes": ["coordination_drill","focus_practice"]}}},
                {"conditioning_workout": {"rating": 74, "data": {"item": "crossfit_box.png", "attributes": ["power_exercise","stamina_build"]}}},
                {"mobility_drill": {"rating": 62, "data": {"item": "foam_rolling.png", "attributes": ["agility_course","flexibility_session"]}}},
                {"deadlift_session": {"rating": 88, "data": {"item": "deadlift.png", "attributes": ["strength_training","power_exercise"]}}},
                {"marathon_training": {"rating": 76, "data": {"item": "marathon.png", "attributes": ["endurance_run","stamina_build"]}}},
                {"hurdle_run": {"rating": 71, "data": {"item": "hurdles.png", "attributes": ["agility_course","sprint_speed"]}}},
                {"soccer_drill": {"rating": 71, "data": {"item": "soccer_dribble.png", "attributes": ["teamwork_drill","stamina_build"]}}},
                {"surfing_practice": {"rating": 66, "data": {"item": "surf_board.png", "attributes": ["balance_challenge","mobility_drill"]}}},
                {"volleyball_training": {"rating": 69, "data": {"item": "volleyball_spike.png", "attributes": ["teamwork_drill","coordination_drill"]}}},
                {"boxing_reaction": {"rating": 71, "data": {"item": "boxing_reaction.png", "attributes": ["reaction_test","stamina_build"]}}},
                {"dart_practice": {"rating": 79, "data": {"item": "dart_throw.png", "attributes": ["precision_training","focus_practice"]}}},
                {"board_strategy": {"rating": 77, "data": {"item": "board_game.png", "attributes": ["strategy_game","precision_training"]}}},
                {"soccer_teamwork": {"rating": 73, "data": {"item": "soccer_game.png", "attributes": ["teamwork_drill","leadership_task"]}}},
                {"orchestra_lead": {"rating": 72, "data": {"item": "orchestra_conductor.png", "attributes": ["leadership_task","focus_practice"]}}},
                {"archery_focus": {"rating": 80, "data": {"item": "archery_target.png", "attributes": ["precision_training","focus_practice"]}}},
                {"vertical_jump": {"rating": 84, "data": {"item": "vertical_jump.png", "attributes": ["power_exercise","strength_training"]}}},
                {"pilates_session": {"rating": 61, "data": {"item": "pilates.png", "attributes": ["flexibility_session","mobility_drill"]}}},
                {"tennis_endurance": {"rating": 72, "data": {"item": "tennis_match.png", "attributes": ["stamina_build","coordination_drill"]}}},
                {"skateboard_control": {"rating": 71, "data": {"item": "skateboard_trick.png", "attributes": ["control_drill","agility_course"]}}},
                {"boxing_timing": {"rating": 69, "data": {"item": "boxing_combo.png", "attributes": ["timing_practice","reaction_test"]}}},
                {"jump_rope_rhythm": {"rating": 68, "data": {"item": "jump_rope_routine.png", "attributes": ["rhythm_training","coordination_drill"]}}},
                {"stair_conditioning": {"rating": 73, "data": {"item": "stair_climb.png", "attributes": ["conditioning_workout","stamina_build"]}}},
                {"hip_mobility": {"rating": 60, "data": {"item": "hip_mobility.png", "attributes": ["mobility_drill","flexibility_session"]}}},
                {"bench_press": {"rating": 86, "data": {"item": "bench_press.png", "attributes": ["strength_training","power_exercise"]}}},
                {"swimming_marathon": {"rating": 75, "data": {"item": "swimming_lap.png", "attributes": ["endurance_run","stamina_build"]}}},
                {"bike_sprint": {"rating": 72, "data": {"item": "bike_sprint.png", "attributes": ["sprint_speed","timing_practice"]}}},
                {"basketball_drill": {"rating": 70, "data": {"item": "basketball_dribble.png", "attributes": ["coordination_drill","teamwork_drill"]}}},
                {"snowboard_balance": {"rating": 65, "data": {"item": "snowboard.png", "attributes": ["balance_challenge","control_drill"]}}},
                {"cycling_marathon": {"rating": 74, "data": {"item": "cycling_marathon.png", "attributes": ["endurance_run","stamina_build"]}}},
                {"acrobatics_control": {"rating": 74, "data": {"item": "acrobatics.png", "attributes": ["agility_course","control_drill"]}}},
                {"soccer_tackle": {"rating": 70, "data": {"item": "soccer_tackle.png", "attributes": ["soccer_drill","coordination_drill"]}}},
                {"rowing_rhythm": {"rating": 68, "data": {"item": "rowing_stroke.png", "attributes": ["rhythm_training","stamina_build"]}}},
                {"boxing_training": {"rating": 75, "data": {"item": "boxing_training.png", "attributes": ["stamina_build","conditioning_workout"]}}},
                {"quarterback_drill": {"rating": 72, "data": {"item": "quarterback_drill.png", "attributes": ["leadership_task","teamwork_drill"]}}}
            ],
            "rules": "rating",
            "length": 5
        }

    

    # this is an example of the format needed to adjust the selected vocab. it assumes these are the current vocab items being used by the core engine. a true value indicates that the item and items with related attributes have a lower preference for the next output cycle. a false rating will emphasize that the item and its related items have a higher preference ranking. these values can be determined in whatever way is deemed necessary within the app the app they are being used in(such as user input, elapsed time, etc). 
    def input_format(self):
        return {
            "deadlift_session": False,
            "power_exercise": False,
            "bench_press": False,
            "strength_training": False,
            "vertical_jump": False,
        }


    def test_input(self):
        input = {}
        for item in self.vocab:
            input[item] = random.choice([True, False, True, False, True, False, None])
        return input
    

    def test(self, tests=10):
        print("\n\n\nINITIAL DATA\n")
        self.initial_rankings(self.test_data())
        self.original_data = self.sort_ratings(self.master_rankings)
        print(self.original_data)
        print("\n\nINITIAL RANKINGS\n")
        print(self.vocab)

        self.original_data = self.test_data()
        input = self.input_format()
        for _ in range(tests):
            self.adjust_rankings(input, self.original_data)
            print("\n\n\n\nADJUSTED DATA\n")
            print(self.sort_ratings(self.master_rankings))
            self.get_vocab(self.master_rankings)
            print("\n\nADJUSTED RANKINGS\n")
            print(self.vocab)
            print("\n\n")
            input = self.test_input()
            print("\n\nnew input")
            print(input)
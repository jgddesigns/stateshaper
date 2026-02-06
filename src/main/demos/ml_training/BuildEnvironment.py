import random
import sys
from .data.environments import environment_data
from .TripTimeline import TripTimeline

class BuildEnvironment:


    def __init__(self, token=1, **kwargs):
        # trip length 1-100
        # break into intervals
        # transitions have increment/decrement style for each attribute based on neighboring intervals. ie low elevation -> high elevation incline number steadily rises between each interval's median, some values change instantly when needed. 
        # intervals can overlap ie low elevation with rain or sun to high elevation with rain or sun. ex.: {"low_elevation": [1, 25], "sun": [1, 15], "rain": [15, 70], "high_elevation": [25, 100]}

        # low to high elevation example
        #
        # low elevation interval = 25
        # high elevation interval = 75
        #
        # trip 0-12.5 environment maintains values correlating to a low elevation, but vary within low elevation
        # trip 12.5-50 values transition from low to high elevation
        # trip 50-100 high elevation are maintained, but vary within high elevation

        self.environments = ["coastal_warm","coastal_cold","foothills","mountains","valley","arctic","urban","town"]

        self.constants = {
            "temperature": {"a": 517, "b": 3, "c": 941},
            "humidity": {"a": 89, "b": 777, "c": 141},
            "light": {"a": 333, "b": 17, "c": 905},
            "elevation": {"a": 701, "b": 255, "c": 39},
            "curves": {"a": 11, "b": 893, "c": 477},
            "road_size": {"a": 619, "b": 5, "c": 821},
            "road_texture": {"a": 147, "b": 961, "c": 23},
            "incline": {"a": 555, "b": 79, "c": 907},
            "incline_variance": {"a": 271, "b": 999, "c": 61},
            "traffic": {"a": 401, "b": 9, "c": 863},
            "hazard_variance": {"a": 731, "b": 187, "c": 49},
            "potential_hazard": {"a": 95, "b": 543, "c": 817},
            "weather_variance": {"a": 667, "b": 1, "c": 359},
            "weather_type": {"a": 213, "b": 887, "c": 27}
        }

        self.current_environment = {
            "environment": "",
            "temperature": 0,
            "humidity": 0,
            "light": 0, 
            "elevation": 0, 
            "curves": 0, 
            "road_size": 0,
            "road_texture": 0,
            "incline": 0,
            "incline_variance": 0, 
            "traffic": 0, 
            "hazard_variance": 0,
            "potential_hazard": [],
            "weather_variance": 0,
            "weather_type": []
        }

        self.max_intervals = 6
        self.trip_duration = 100
        self.intervals = []
        self.deviation = 20
        self.token = token




    def get_token(self, random=False):
        return self.token if random == False else random.randint(1, 9999)


    def set_token(self, token):
        self.token = token


    def create_environment(self, token, adjust=1):
        print("start environment")
        print(f"token: {token}")
        intervals = []
        interval_count = 1 + (token % self.max_intervals) + 1
        print(f"interval count {interval_count}")
        current = 0
        while len(intervals) < interval_count: 
            multiplier = 3 if len(intervals) % 2 == 0 else 5
            interval_range = self.get_range(current, intervals, interval_count, token) 
            environment = self.environments[(token * (len(intervals) + 1) * multiplier * adjust)  % len(self.environments)]
            if self.check_included(intervals, environment) == False:
                interval_range[1] = 100 if interval_count - len(intervals) < 2 else interval_range[1]
                intervals.append({"environment": environment, "range": interval_range, "data": self.get_environment(token, environment, multiplier * adjust)})  
            else:
                adjust += 1
                intervals[len(intervals)-1]["range"][1] = 100 if len(intervals) == interval_count else intervals[len(intervals)-1]["range"][1]
            current = intervals[len(intervals)-1]["range"][1]
            if current >= 100:
                print("environments created")
                print(intervals)
                return intervals
    

    def check_included(self, intervals, environment):
        return len([i for i in intervals if i["environment"] == environment]) > 0


    def get_range(self, current, intervals, interval_count, token):
        min_range = 10
        remaining = self.trip_duration - current
        start = current
        end = current + (token % remaining) if len(intervals) < interval_count - 1 else 100
        end = end + min_range if current - end < min_range else end
        end = 100 if end > 100 or interval_count - len(intervals) < 2 else end
        return [start, end]


    def get_environment(self, token, environment, multiplier):
        current_environment = {}
        current_environment["environment"] = environment
        for value in environment_data[environment].items():
            current_environment[value[0]] = self.get_value(token, value[0], value[1], multiplier) if isinstance(value[1], list) == False else self.get_list(token, value[0], value[1], multiplier)
        return current_environment


    def get_deviation(self, token, constant):
        return round(((((token + constant) % self.deviation) / self.deviation)/5), 2) if token % 2 == 0 else -round(((((token + constant) % self.deviation) / self.deviation)/5), 2)
    

    def get_constant(self, token, attribute, multiplier):
        constants = [int(str(i[1])[:1]) % int(str(token*multiplier)[:1]) for i in self.constants[attribute].items()]
        matching = min(constants)
        return list(self.constants[attribute].values())[constants.index(matching)]


    def get_value(self, token, environment, value, multiplier):
        constant = self.get_constant(token, environment, multiplier)
        final = round((value + self.get_deviation(token, constant)), 2) if environment != "hazard_variance" else value
        return 0 if final < 0 else final if final < 1 else 1 
    

    def get_list(self, token, environment, value, multiplier):
        constant = self.get_constant(token, environment, multiplier)
        return value[(token * constant) % len(value)]
    

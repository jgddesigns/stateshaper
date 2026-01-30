import copy
import random
import sys
import time
from .data.environments import environment_data

class TripTimeline:


    def __init__(self, trip={'environment': 'town', 'range': [0, 5], 'data': {'environment': 'town', 'temperature': 0.48, 'humidity': 0.26, 'light': 0.42, 'elevation': 0.24, 'curves': 0.09, 'road_size': 0.31, 'road_texture': 0.23, 'incline': 0.2, 'incline_variance': 0.04, 'traffic': 0.29, 'hazard_variance': 0.01, 'potential_hazard': 'cyclist', 'weather_variance': 0.18, 'weather_type': 'rain'}}, token=5, **kwargs):
        # trip length 1-100
        # break into intervals
        # transitions have increment/decrement style for each attribute based on neighboring intervals. ie low elevation -> high elevation incline number steadily rises between each interval's median, some values change instantly when needed. 
        # intervals can overlap ie low elevation with rain or sun to high elevation with rain or sun. ex.: {"low_elevation": [1, 25], "sun": [1, 15], "rain": [15, 70], "high_elevation": [25, 100]}
        self.trip = trip
        self.current_trip = trip["environment"]
        self.current_interval = copy.deepcopy(trip["environment"][0])
        self.total_trip = copy.deepcopy(trip["environment"][0])
        self.token = token
        try:
            self.next_interval = trip[1] 
        except:
            self.next_interval = None

        self.max_counter = 100

        self.trip_counter = 0 
        self.trip_length = 100 #lets say 1 is 1 mile. nothing fancy yet (real times). irl 1 mile takes longer than 1 second.

        self.run = False
        self.end = False

        self.hazard_fail = 2

        self.trip_attributes =  {
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
            "weather_variance": 0,
        }

        self.constants = {
            "temperature": {"a": 517, "b": 3, "c": 941},
            "humidity": {"a": 89, "b": 775, "c": 141},
            "light": {"a": 319, "b": 17, "c": 905},
            "elevation": {"a": 701, "b": 255, "c": 39},
            "curves": {"a": 11, "b": 893, "c": 477},
            "road_size": {"a": 619, "b": 5, "c": 821},
            "road_texture": {"a": 147, "b": 961, "c": 23},
            "incline": {"a": 555, "b": 79, "c": 907},
            "incline_variance": {"a": 271, "b": 959, "c": 61},
            "traffic": {"a": 401, "b": 9, "c": 863},
            "hazard_variance": {"a": 731, "b": 183, "c": 49},
            "potential_hazard": {"a": 95, "b": 543, "c": 817},
            "weather_variance": {"a": 667, "b": 1, "c": 359},
            "weather_type": {"a": 213, "b": 887, "c": 27}
        }

        self.measured = {
            "gradual": ["temperature", "humidity", "elevation", "incline"],
            "varients": [["incline", "incline_variance"], ["potential_hazard", "hazard_variance"], ["weather_type", "weather_variance"]],
            "instant": ["light", "road_size", "road_texture", "incline_variance", "traffic", "hazard_variance", "potential_hazard", "weather_variance", "weather_type"]
        }

        self.hazard_data = []
        self.steering_precision = []
        self.speed_precision = [] 
        self.stop_precision = [] 
        self.rule_precision = []

    


    def start_trip(self):
        self.trip_progress()
        return self.trip


    def trip_progress(self):
        self.check_intervals()
        print(f"\n\n\n\nCurrent Interval: {self.current_interval['environment']}, Range: {self.current_interval['range']}")
        print(f"\n{self.current_interval}")
        if self.next_interval != None:
            print(f"\n\nNext Interval: {self.next_interval['environment']}, Range: {self.next_interval['range']}")
            print(f"\n{self.next_interval}\n\n")
        self.run_timer()
        

    def check_intervals(self):
        if self.trip_counter > 0:
            self.current_interval = copy.deepcopy(self.next_interval) 
            self.total_trip = copy.deepcopy(self.next_interval)
        if len(self.current_trip) > 1 :
            self.next_interval = self.check_next()
            self.compare_intervals() if self.next_interval != None else None


    def check_next(self):
        try:
            return self.current_trip[self.current_trip.index(self.current_interval)+1]
        except:
            print("End of possible environments in this trip.")
            return None
        

    def compare_intervals(self):
        for attribute in self.trip_attributes:
            self.set_attribute(attribute) 
        print(f"\n\nnext trip interval set: {self.current_interval}")


    def set_attribute(self, attribute):
        self.trip_attributes[attribute] = self.change_rate(attribute) if attribute in self.measured["gradual"] else self.next_interval["data"][attribute]


    def change_rate(self, attribute):
        try: 
            return round(((self.next_interval["data"][attribute] - self.current_interval["data"][attribute])) / ((self.current_interval["range"][1] - self.current_interval["range"][0])), 6)
        except:
            pass


    def run_timer(self, timer=False):
        if self.end == False:
            self.trip_counter += 1
            self.adjust_values()
            self.hazard_check()
            self.steering_check()
            self.speed_check()
            self.stop_check()
            self.rules_check()
            self.end_check()
            # time.sleep(1) if timer == True else None 
        return True
        

    def adjust_values(self):
        print(f"\n\n\n\nTrip Counter: {self.trip_counter}")
        print(f"Environment: {self.current_interval['environment']}, Range: {self.current_interval['range']}")
        print(self.token)
        print(self.trip_attributes)
        for attribute in self.trip_attributes:
            self.total_trip["data"][attribute] = (self.total_trip["data"][attribute] + self.trip_attributes[attribute]) if attribute in self.measured["gradual"] else self.trip_attributes[attribute]

        if self.next_interval != None:
            if self.trip_counter == self.next_interval["range"][0]:
                self.run = False
                for attribute in self.trip_attributes:
                    self.total_trip["data"][attribute] = round(self.total_trip["data"][attribute], 2) 

                self.interval_end()
    

    def end_check(self):
        if self.trip_counter >= self.trip_length and self.end == False:
            print("\n\nend of trip")
            print("\n\nhazards encountered\n")
            print(self.hazard_data)
            self.trip_data = {"hazard_data": self.hazard_data, "steering_precision": self.steering_precision, "speed_precision": self.speed_precision, "stop_precision": self.stop_precision, "rule_precision": self.rule_precision}
            self.end = True
            # print("\n\ntrip")
            # print(self.trip)
        else:
            self.run_timer()
            

    def interval_end(self):
        print("\n\n\nend of interval")
        print("\n\nnext interval")
        print(self.next_interval)
        print("\n\n")
        self.trip_progress()


    def hazard_check(self):
        print(f"\ncompare hazard variance")
        print(f"{self.current_interval['data']['hazard_variance']}, {self.hazard_chance()}\n")
        if self.hazard_chance() < self.current_interval["data"]["hazard_variance"]:
            print("hazard encountered")
            self.handle_hazard(True) if self.fail_check() else self.handle_hazard(False)
    

    def steering_check(self):
        pass

    def speed_check(self):
        pass

    def stop_check(self):
        pass

    def rules_check(self):
        pass


    def fail_check(self):
        print(round(self.compare_constants("hazard_variance") * ((self.token * self.trip_counter) if self.trip_counter % 2 == 0 else (self.token * self.trip_counter * self.trip_counter))))
        return round(self.compare_constants("hazard_variance") * ((self.token * self.trip_counter) if self.trip_counter % 2 == 0 else (self.token * self.trip_counter * self.trip_counter))) % self.hazard_fail == 0


    def hazard_chance(self):
        return (((self.trip_counter + self.compare_constants("hazard_variance")) * (self.token * self.compare_constants("hazard_variance") + (round(self.compare_constants("hazard_variance"))/self.trip_counter))) % 100) / 100


    def handle_hazard(self, fail):
        self.hazard_data.append({"environment": self.current_interval["environment"], "hazard": self.current_interval["data"]["potential_hazard"], "location": self.trip_counter, "result": fail})


    def compare_constants(self, variance):
        compare = [(i * round(self.token * int(self.current_interval["data"][variance]) * int(self.trip_counter)) % self.token) for i in list(self.constants[variance].values())]
        matching = compare.index(min(compare))
        return self.constants[variance][list(self.constants[variance].keys())[matching]]
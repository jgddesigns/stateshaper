import random

from .BuildEnvironment import BuildEnvironment
from .data.vehicles import vehicles

class MachineLearning:


    def __init__(self, token=5, **kwargs):

        self.vehicle = {
            "torque": 0,                # 0 (pulls nothing) - 1 (pulls anything)
            "acceleration": 0,          # 0-60 rating | 0 (stopped) - 1 (instant)
            "speed": 0,                 # top speed | 0 (stopped) - 1 (200mph)
            "durability": 0,            # against environment | (anything harms it) - 1 (invincible)
            "tread": 0,                 # grip on road | 0 (no grip) - 1 (super glue)
            "size": 0,                  # space it fills | 0 (invisible) - 1 (mountain)
            "tank": 0,                  # size of gas tank/battery charge | 0 (none) - 1 (infinite)
            "efficiency": 0             # mpg or kwh | 0 (instant drain) - 1 (no drain)
        }

        self.attributes = {
            "torque": self.get_torque,
            "acceleration": self.get_acceleration,
            "speed": self.get_speed,
            "durability": self.get_durability,
            "tread": self.get_tread,
            "size": self.get_size,
            "tank": self.get_tank,
            "efficiency": self.get_efficiency,
        }


        self.tensors = {
            "incline": 0,               # how steep is the road? | 0 (horizontal) - 1 (vertical)
            "curve": 0,                 # curves in current range -1/4 mile < 1/4 mile | 0 (straight) - 1 (90 degree turn)
            "temperature": 0,           # current outer temperature | 0 (-120 F) - 1 (120 F)
            "space": 0,                 # amount of lanes in road | 0 (no space) - 1 (open pasture)
            "traffic": 0,               # density fof traffic | 0 (just you) - 1 (traffic jam)
            "traction": 0,              # tires grip on the road | 0 (iced/oil road) - 1 (perfect grip)
            "abrasion": 0,              # is the road smooth, or uneven? | 0 (smooth pavement) - 1 (jagged offroad rocks)
        }

        self.environment = {
            "incline": self.get_incline,          
            "curve": self.get_curve,              
            "temperature": self.get_temperature,  
            "space": self.get_space,              
            "traffic": self.get_traffic,          
            "traction": self.get_traction,        
            "abrasion": self.get_abrasion,         
        }

        self.constants = {
            "a": 3,
            "b": 7,
            "c": 11,
            "d": 23,
            "e": 31,
            "f": 57,
            "g": 65, 
            "h": 71,
            "i": 85,
            "j": 91
        }

        self.mod = 100

        self.build_environment = BuildEnvironment(token)
 
        self.one_vehicle = None
        self.one_tensors = None




    def test_logic(self, token_count=5, one_vehicle=0, one_tensors=0):
        for _ in range(token_count):
            random_vehicle = True if random.randint(0, 100) / 100 < one_vehicle else None
            random_tensors = True if random.randint(0, 100) / 100 < one_tensors else None
            self.current_test(random.randint(1, 9999), one_vehicle=random_vehicle, one_tensors=random_tensors)


    def current_test(self, token=None, one_vehicle=None, one_tensors=None): 
        token = random.randint(1, 9999) if not token else token
        self.build_environment = BuildEnvironment(token)
        vehicle = self.get_vehicle(token) if not one_vehicle or self.one_vehicle == None else self.one_vehicle
        self.one_vehicle = vehicle 
        tensors = self.get_tensors(token) if not one_tensors or self.one_tensors == None  else self.one_tensors
        self.one_tensors = tensors

        random_txt = "Random"
        repeat_txt = "Repeat"
        print("\n\nNew ML Training Test Created\n")
        print(f"Vehicle: {repeat_txt if one_vehicle else random_txt}, Tensors: {repeat_txt if one_tensors else random_txt}\n")
        print({"vehicle": vehicle, "tensors": tensors})
        print("\n\n\n")
        environment = self.build_environment.create_environment(token)
        return {"vehicle": vehicle, "tensors": tensors, "environment": environment}


    def get_vehicle(self, token):
        # vehicle = {}
        # for item in self.attributes.items():
        #     vehicle[item[0]] = item[1](token)
        # return vehicle
        vehicle = token % len(vehicles)
        return vehicles[vehicle]
    

    def get_tensors(self, token):
        tensors = {}
        for item in self.environment.items():
            tensors[item[0]] = item[1](token)
        return tensors


    def get_torque(self, token):
        return  round(((((token * self.constants["b"]) * self.constants["d"]) % self.mod) / self.mod), 2)


    def get_acceleration(self, token):
        return round(((((token * token * self.constants["a"]) * self.constants["e"]) % self.mod) / self.mod), 2)


    def get_speed(self, token):
        return round(((((token + (token * self.constants["c"]) * self.constants["f"]) * token) % self.mod) / self.mod), 2)


    def get_durability(self, token):
        return round((((token * self.constants["f"] * self.constants["a"])) % self.mod) / self.mod, 2)


    def get_tread(self, token):
        return round((((abs(token-self.constants["f"]) * self.constants["h"] * self.constants["a"])) % self.mod) / self.mod, 2)
    

    def get_size(self, token):
        return round((((token * token * self.constants["g"])) % self.mod) / self.mod, 2)


    def get_tank(self, token):
        return round((((token * self.constants["c"] * self.constants["j"] + self.constants["e"])) % self.mod) / self.mod, 2)


    def get_efficiency(self, token):
        return round((((token + token * self.constants["a"] * self.constants["f"])) % self.mod) / self.mod, 2)


    def get_incline(self, token):
        return round((((token + (token * self.constants["i"]) * self.constants["b"])) % self.mod) / self.mod, 2)


    def get_curve(self, token):
        return round((((token + self.constants["c"]) * (self.constants["e"] - self.constants["b"])) % self.mod) / self.mod, 2)


    def get_temperature(self, token):
        return round((((token * token * token) * (self.constants["d"] - self.constants["e"] + self.constants["i"])) % self.mod) / self.mod, 2)


    def get_space(self, token):
        return round(((token * self.constants["j"] * (self.constants["b"] + self.constants["c"] + self.constants["c"])) % self.mod) / self.mod, 2)


    def get_traffic(self, token):
        return round(((token + (self.constants["c"] * (self.constants["d"] + self.constants["e"]))) % self.mod) / self.mod, 2)
    

    def get_traction(self, token):
        return round(((abs(token - (self.constants["a"] * (self.constants["d"] + self.constants["f"])))) % self.mod) / self.mod, 2)


    def get_abrasion(self, token):
        return round(((token * (self.constants["e"] * self.constants["f"] * self.constants["g"])) % self.mod) / self.mod, 2)
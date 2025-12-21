import sys
from typing import List



class Morph:


    def __init__(self):
        pass

    def morph(self, shaper, iteration):
        for i in range(len(shaper["seed"])):
            shaper["seed"][i] = int(shaper["constants"]["b"] * shaper["constants"]["a"] * (shaper["constants"]["d"]) / shaper["constants"]["c"]) * (iteration + i + shaper["constants"]["c"]) % shaper["mod"]

        return shaper["seed"] 


    def morph_one(self, shaper, iteration):
        seed = int(shaper["constants"]["b"] * shaper["constants"]["a"] * (shaper["constants"]["d"]) / shaper["constants"]["c"]) * (iteration + shaper["constants"]["c"]) % shaper["mod"]
        shaper["seed"].pop(0)
        shaper["seed"].append(seed) 
        return shaper["seed"] 
    

    def morph_reverse(self, shaper, iteration):
        seed = int(shaper["constants"]["b"] * shaper["constants"]["a"] * (shaper["constants"]["d"]) / shaper["constants"]["c"]) * (iteration + shaper["constants"]["c"]) % shaper["mod"]
        shaper["seed"].pop(len(shaper["seed"])-1)
        shaper["seed"] = [seed] + shaper["seed"]
        return shaper["seed"]
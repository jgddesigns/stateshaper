
TINY STATE COMPRESSION




With Command Line


    1. pip install tiny-state 


    2. Then, from cmd or shell run: 


        A) First encode the personalization data

        
            tiny-state encode -example.json

                Input Format:

                    Example at bottom of page.

                Output:

                    seed: ABC12345 (Tiny State)
                    subset: OPQCDERST4 (Raw State)


            These values can be stored and used to recreate the personalization stream within the Stateshaper Engine.



        B) Then, when needed, the seeds can be decoded and used with the Stateshaper Engine in conjuction with the personalization plugin (including custom solutions).
        

            tiny-state decode -seed -subset

                Input Format (outputted data from input):

                    seed: ABC12345 
                    subset: OPQCDERST4

                Output:

                    example.txt (bottom of page)



                



Using TinyState Class


    1. Start Class Instance

        from tools.tiny_state.TinyState import TinyState
    
        tiny_state = TinyState()


    2. Create Seeds (create a set of seeds to define personalization based on a json dataset)
    
        seeds = self.tiny_state.get_seed(example.json)
    
        data example - [AAA02003, OPQ345LMNX]



    3. Decode Seeds (get original personalization)

        self.tiny_state.rebuild_data(seed, subset)




Whenever the original json data (example.json) is modified, re-encode it to a new set of seeds.







Data Input Example


example.json

data = {
            "team": {
                "rating": 55,
                "data": [
                    {"item": "football.png", "attributes": ["team", "contact", "outdoor"]},
                    {"item": "basketball.png", "attributes": ["team", "indoor", "fast-paced"]},
                    {"item": "soccer.png", "attributes": ["team", "endurance", "outdoor"]}
                ]
            },

            "individual": {
                "rating": 47,
                "data": [
                    {"item": "tennis.png", "attributes": ["individual", "court", "precision"]},
                    {"item": "golf.png", "attributes": ["individual", "outdoor", "precision"]},
                    {"item": "climbing.png", "attributes": ["individual", "strength", "indoor"]}
                ]
            },

            "combat": {
                "rating": 71,
                "data": [
                    {"item": "boxing.png", "attributes": ["combat", "individual", "indoor"]},
                    {"item": "mma.png", "attributes": ["combat", "discipline", "individual"]},
                    {"item": "wrestling.png", "attributes": ["combat", "grappling", "mat"]}
                ]
            },

            "water": {
                "rating": 38,
                "data": [
                    {"item": "swimming.png", "attributes": ["water", "endurance", "individual"]},
                    {"item": "surfing.png", "attributes": ["water", "balance", "outdoor"]},
                    {"item": "waterpolo.png", "attributes": ["water", "team", "endurance"]}
                ]
            },

            "cycling": {
                "rating": 84,
                "data": [
                    {"item": "cycling.png", "attributes": ["cycling", "endurance", "outdoor"]},
                    {"item": "mountain_biking.png", "attributes": ["cycling", "terrain", "outdoor"]},
                    {"item": "bmx.png", "attributes": ["cycling", "stunts", "individual"]}
                ]
            },

            "track": {
                "rating": 59,
                "data": [
                    {"item": "sprinting.png", "attributes": ["track", "speed", "individual"]},
                    {"item": "marathon.png", "attributes": ["track", "endurance", "road"]},
                    {"item": "relay.png", "attributes": ["track", "team", "speed"]}
                ]
            },

            "winter": {
                "rating": 66,
                "data": [
                    {"item": "skiing.png", "attributes": ["winter", "outdoor", "individual"]},
                    {"item": "snowboarding.png", "attributes": ["winter", "balance", "outdoor"]},
                    {"item": "biathlon.png", "attributes": ["winter", "endurance", "precision"]}
                ]
            },

            "recreation": {
                "rating": 42,
                "data": [
                    {"item": "skateboarding.png", "attributes": ["recreation", "balance", "stunts"]},
                    {"item": "surfskate.png", "attributes": ["recreation", "outdoor", "balance"]},
                    {"item": "parkour.png", "attributes": ["recreation", "agility", "urban"]}
                ]
            },

            "precision": {
                "rating": 90,
                "data": [
                    {"item": "archery.png", "attributes": ["precision", "focus", "individual"]},
                    {"item": "shooting.png", "attributes": ["precision", "control", "individual"]},
                    {"item": "golf_putting.png", "attributes": ["precision", "technique", "individual"]}
                ]
            },

            "digital": {
                "rating": 88,
                "data": [
                    {"item": "esports.png", "attributes": ["digital", "competitive", "team"]},
                    {"item": "sim_racing.png", "attributes": ["digital", "precision", "individual"]},
                    {"item": "virtual_chess.png", "attributes": ["digital", "strategy", "mental"]}
                ]
            }
        }
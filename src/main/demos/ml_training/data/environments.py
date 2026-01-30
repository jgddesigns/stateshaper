# temperature       0 (-120F) - 1 (120F)
# humidity          0 (0%) - 1 (100%)
# light             0 (dark) - 1 (light)
# elevation         0 (flat) - 1 (highest mountain)
# curves            0 (straight) - 1 (90 degrees)
# road_size         0 (bike lane) - 1 (5 lane freeway)
# road_texture      0 (smooth) - 1 (jagged rocks)
# incline           0 (horizontal) - 1 (vertical)
# incline_variance  0 (steady) - 1 (fluctuation)
# traffic           0 (just you) - 1 (gridlock)
# hazard_variance   0 (peace) - 1 (chaos)
# potential_hazard  ["crash","chemical_spill","oil_spill","animal_crossing","fallen_tree","ice_road","fire","pedestrian","cyclist"]
# weather_variance  0 (steady) - 1 (fluctuation)
# weather_type     ["sun","rain","snow","sleet","blizzard","hail","wind","fog","cloudy","lightning","tornado", "dust"]


environment_data = {
    "desert": {
        "temperature": .9,
        "humidity": .3,
        "light": 1,
        "elevation": .05,
        "curves": 0,
        "road_size": .3,
        "road_texture": .4,
        "incline": 0,
        "incline_variance": 0,
        "traffic": .05,
        "hazard_variance": .01,
        "potential_hazard": ["crash", "animal_crossing", "cyclist"],
        "weather_variance": 0,
        "weather_type": ["sun", "sand", "dust"]
    },
    "coastal_warm": {
        "temperature": .7,
        "humidity": .6,
        "light": .8,
        "elevation": 0,
        "curves": .5,
        "road_size": .3,
        "road_texture": .2,
        "incline": .2,
        "incline_variance": .5,
        "traffic": .4,
        "hazard_variance": .025,
        "potential_hazard": ["crash", "animal_crossing", "fallen_tree", "cyclist", "cliff"],
        "weather_variance": .7,
        "weather_type": ["sun", "rain", "wind", "fog", "cloudy"]
    },
    "coastal_cold": {
        "temperature": .3,
        "humidity": .4,
        "light": .4,
        "elevation": 0,
        "curves": .5,
        "road_size": .3,
        "road_texture": .2,
        "incline": .2,
        "incline_variance": .5,
        "traffic": .4,
        "hazard_variance": .035,
        "potential_hazard": ["crash", "animal_crossing", "fallen_tree", "ice_road", "cyclist", "cliff"],
        "weather_variance": .35,
        "weather_type": ["rain", "snow", "sleet", "blizzard", "hail", "wind", "fog", "cloudy", "lightning"]
    },
    "foothills": {
        "temperature": .4,
        "humidity": .5,
        "light": .75,
        "elevation": .35,
        "curves": .6,
        "road_size": .25,
        "road_texture": .3,
        "incline": .4,
        "incline_variance": .7,
        "traffic": .3,
        "hazard_variance": .012,
        "potential_hazard": ["crash", "animal_crossing", "fallen_tree", "ice_road", "fire", "cyclist", "cliff"],
        "weather_variance": .6,
        "weather_type": ["sun", "rain", "snow", "hail", "wind", "cloudy", "lightning"]
    },
    "mountains": {
        "temperature": .3,
        "humidity": .3,
        "light": .4,
        "elevation": .7,
        "curves": .7,
        "road_size": .25,
        "road_texture": .35,
        "incline": .6,
        "incline_variance": .5,
        "traffic": .2,
        "hazard_variance": .025,
        "potential_hazard": ["crash", "animal_crossing", "fallen_tree", "ice_road", "fire", "cliff"],
        "weather_variance": .4,
        "weather_type": ["sun", "rain", "snow", "sleet", "blizzard", "hail", "wind", "cloudy", "lightning", "tornado"]
    },
    "valley": {
        "temperature": .4,
        "humidity": .4,
        "light": .4,
        "elevation": .1,
        "curves": 0,
        "road_size": .35,
        "road_texture": .2,
        "incline": 0,
        "incline_variance": 0,
        "traffic": .4,
        "hazard_variance": .01,
        "potential_hazard": ["crash", "fire"],
        "weather_variance": .4,
        "weather_type": ["sun", "rain", "sleet", "hail", "wind", "fog", "cloudy", "lightning", "tornado"]
    },
    "arctic": {
        "temperature": .1,
        "humidity": .3,
        "light": .3,
        "elevation": .3,
        "curves": .3,
        "road_size": .3,
        "road_texture": .4,
        "incline": .1,
        "incline_variance": .25,
        "traffic": .1,
        "hazard_variance": .04,
        "potential_hazard": ["crash", "animal_crossing", "ice_road"],
        "weather_variance": .4,
        "weather_type": ["snow", "sleet", "blizzard", "wind", "cloudy"]
    },
    "urban": {
        "temperature": .5,
        "humidity": .35,
        "light": .5,
        "elevation": .5,
        "curves": .05,
        "road_size": .3,
        "road_texture": .2,
        "incline": .1,
        "incline_variance": .2,
        "traffic": .75,
        "hazard_variance": .02,
        "potential_hazard": ["crash", "chemical_spill", "oil_spill", "pedestrian", "cyclist"],
        "weather_variance": .4,
        "weather_type": ["sun", "rain", "snow", "sleet", "wind", "fog", "cloudy"]
    },
    "town": {
        "temperature": .5,
        "humidity": .4,
        "light": .6,
        "elevation": .3,
        "curves": .25,
        "road_size": .35,
        "road_texture": .35,
        "incline": .2,
        "incline_variance": .2,
        "traffic": .35,
        "hazard_variance": .01,
        "potential_hazard": ["crash", "animal_crossing", "fallen_tree", "ice_road", "fire", "pedestrian", "cyclist"],
        "weather_variance": .3,
        "weather_type": ["sun", "rain", "snow", "blizzard", "hail", "wind", "cloudy"]
    }
}
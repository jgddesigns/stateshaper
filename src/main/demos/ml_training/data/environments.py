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
        "temperature": 0.9,
        "humidity": 0.3,
        "light": 1.0,
        "elevation": 0.05,
        "curves": 0.0,
        "road_size": 0.3,
        "road_texture": 0.4,
        "incline": 0.0,
        "incline_variance": 0.0,
        "traffic": 0.05,
        "hazard_variance": 0.01,
        "potential_hazard": 0.25,
        "weather_variance": 0.0,
        "weather_type": 0.2
    },
    "coastal_warm": {
        "temperature": 0.7,
        "humidity": 0.6,
        "light": 0.8,
        "elevation": 0.0,
        "curves": 0.5,
        "road_size": 0.3,
        "road_texture": 0.2,
        "incline": 0.2,
        "incline_variance": 0.5,
        "traffic": 0.4,
        "hazard_variance": 0.025,
        "potential_hazard": 0.45,
        "weather_variance": 0.7,
        "weather_type": 0.5
    },
    "coastal_cold": {
        "temperature": 0.3,
        "humidity": 0.4,
        "light": 0.4,
        "elevation": 0.0,
        "curves": 0.5,
        "road_size": 0.3,
        "road_texture": 0.2,
        "incline": 0.2,
        "incline_variance": 0.5,
        "traffic": 0.4,
        "hazard_variance": 0.035,
        "potential_hazard": 0.6,
        "weather_variance": 0.35,
        "weather_type": 0.7
    },
    "foothills": {
        "temperature": 0.4,
        "humidity": 0.5,
        "light": 0.75,
        "elevation": 0.35,
        "curves": 0.6,
        "road_size": 0.25,
        "road_texture": 0.3,
        "incline": 0.4,
        "incline_variance": 0.7,
        "traffic": 0.3,
        "hazard_variance": 0.012,
        "potential_hazard": 0.65,
        "weather_variance": 0.6,
        "weather_type": 0.6
    },
    "mountains": {
        "temperature": 0.3,
        "humidity": 0.3,
        "light": 0.4,
        "elevation": 0.7,
        "curves": 0.7,
        "road_size": 0.25,
        "road_texture": 0.35,
        "incline": 0.6,
        "incline_variance": 0.5,
        "traffic": 0.2,
        "hazard_variance": 0.025,
        "potential_hazard": 0.75,
        "weather_variance": 0.4,
        "weather_type": 0.85
    },
    "valley": {
        "temperature": 0.4,
        "humidity": 0.4,
        "light": 0.4,
        "elevation": 0.1,
        "curves": 0.0,
        "road_size": 0.35,
        "road_texture": 0.2,
        "incline": 0.0,
        "incline_variance": 0.0,
        "traffic": 0.4,
        "hazard_variance": 0.01,
        "potential_hazard": 0.2,
        "weather_variance": 0.4,
        "weather_type": 0.65
    },
    "arctic": {
        "temperature": 0.1,
        "humidity": 0.3,
        "light": 0.3,
        "elevation": 0.3,
        "curves": 0.3,
        "road_size": 0.3,
        "road_texture": 0.4,
        "incline": 0.1,
        "incline_variance": 0.25,
        "traffic": 0.1,
        "hazard_variance": 0.04,
        "potential_hazard": 0.55,
        "weather_variance": 0.4,
        "weather_type": 0.8
    },
    "urban": {
        "temperature": 0.5,
        "humidity": 0.35,
        "light": 0.5,
        "elevation": 0.5,
        "curves": 0.05,
        "road_size": 0.3,
        "road_texture": 0.2,
        "incline": 0.1,
        "incline_variance": 0.2,
        "traffic": 0.75,
        "hazard_variance": 0.02,
        "potential_hazard": 0.6,
        "weather_variance": 0.4,
        "weather_type": 0.55
    },
    "town": {
        "temperature": 0.5,
        "humidity": 0.4,
        "light": 0.6,
        "elevation": 0.3,
        "curves": 0.25,
        "road_size": 0.35,
        "road_texture": 0.35,
        "incline": 0.2,
        "incline_variance": 0.2,
        "traffic": 0.35,
        "hazard_variance": 0.01,
        "potential_hazard": 0.5,
        "weather_variance": 0.3,
        "weather_type": 0.6
    }
}

from demos.ml_training.BuildEnvironment import BuildEnvironment
from demos.ml_training.MachineLearning import MachineLearning
from demos.ml_training.TripTimeline import TripTimeline
import random

# build = BuildEnvironment()

ml = MachineLearning()



for _ in range(10000):
    token = random.randint(1, 9999)
    test = ml.current_test(token)

    trip = TripTimeline(test, token)
    print(trip.start_trip())

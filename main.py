import json
import random
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from src.main.demos.ml_training.TripTimeline import TripTimeline
from src.main.demos.ml_training.MachineLearning import MachineLearning
from src.main.stateshaper import RunEngine
from fastapi.middleware.cors import CORSMiddleware


count = 10

app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    #allow_origins=["https://stateshaper-graphics.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# run = RunEngine()
ml = MachineLearning()


class Input(BaseModel):
    message: str



with open("example_data/tokens.json", "r") as f:
    data = json.loads(f.read())
    f.close()
run = RunEngine(data, token_count=50)
run.start_engine()
# state = [random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973)]
state=[1]
run.define_engine(state=state)
tokens = run.run_engine()
trip = TripTimeline()
run_trip = RunEngine(data, token_count=50)
run_trip.start_engine()
run_trip.define_engine(state=state)


@app.post("/api/start")
def forward():
    run.start_engine()
    run.define_engine(state=state)
    token = run.one_token()
    test = ml.current_test(token)
    run_trip.start_engine()
    run_trip.define_engine(state=state)
    trip.reset_trip()
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(), run.engine]}}


@app.post("/api/forward")
def forward():
    token = run.one_token()
    test = ml.current_test(token)
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(), run.engine]}}


@app.post("/api/reverse")
def reverse():
    token = run.reverse_one()
    test = ml.current_test(token)
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(), run.engine]}}


@app.post("/api/trip")
def run_test(input: Input):
    input = json.loads(input.message)
    token = run_trip.one_token()
    trip.set_trip(token, input["environment"])
    trip.start_trip()
    test = trip.run_timer(False, True)
    
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(state=state), run.engine]}}


@app.post("/api/reset")
def forward():
    # run.define_engine(state=state)
    run_trip.start_engine()
    run_trip.define_engine(state=state)
    trip.reset_trip()
    return {"response": {}}
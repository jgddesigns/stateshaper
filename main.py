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
state = [random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973), random.randint(1, 9973)]
run.define_engine(state=state)
tokens = run.run_engine()


@app.post("/api/forward")
def forward():
    token = run.one_token()
    test = ml.current_test(token)
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(state=state), run.engine]}}


@app.post("/api/reverse")
def reverse():
    token = run.reverse_one()
    test = ml.current_test(token)
    return {"response": {"test": test, "token": token, "seed": [run.get_seed(state=state), run.engine]}}


@app.post("/api/run_test")
def run_test(input: Input):
    input = json.loads(input.message)
    trip = TripTimeline(input["token"], input["environment"])
    test = trip.start_trip()
    return {"response": {"trip": trip, "test": test, "token": input["token"], "seed": [run.get_seed(state=state), run.engine]}}
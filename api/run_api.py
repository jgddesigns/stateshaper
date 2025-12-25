from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.main.connector.Connector import Connector

from src.main.run import RunEngine
import json

run = RunEngine()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    message: str


@app.post("/api/start")
def process():
    output = run.plugin.get_data()
    run.connector = Connector(output)
    run.run_engine()
    return {"response": {"output": output, "ratings": run.plugin.interests, "seed": run.seed}}


@app.post("/api/process")
def process(input: Input):
    input = json.loads(input.message)
    clean_input(input)
    new_data = run.plugin.change_data(input)
    run.connector = Connector(new_data)
    run.run_engine()
    return {"response": {"output": new_data, "ratings": run.plugin.interests, "seed": run.seed}}


@app.post("/api/test_run")
def process(input: Input):
    return json.loads(input.message)


def clean_input(input):
    for item in input.items():
        input[item[0]] = int(item[1])
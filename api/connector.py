from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

from fastapi.middleware.cors import CORSMiddleware

from src.main.classes.connector.Connector import Connector

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
    ads = run.plugin.get_data()
    run.connector = Connector(ads)
    run.run_engine()
    return {"response": {"ads": ads, "ratings": run.plugin.interests, "seed": run.seed}}


@app.post("/api/process")
def process(input: Input):
    input = json.loads(input.message)
    clean_input(input)
    new_data = run.plugin.change_data(input)
    run.connector = Connector(new_data)
    run.run_engine()
    return {"response": {"ads": new_data, "ratings": run.plugin.interests, "seed": run.seed}}


def clean_input(input):
    for item in input.items():
        input[item[0]] = int(item[1])


handler = Mangum(app)
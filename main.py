import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from src.main.classes.connector.Connector import Connector
from src.main.run import RunEngine
from fastapi.middleware.cors import CORSMiddleware
run = RunEngine()

app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],  
    allow_origins=["https://stateshaper-ads.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    message: str


@app.post("/api/start")
def start():
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


# @app.get("/")
# def read_root():
#     ads = run.plugin.get_data()
#     run.connector = Connector(ads)
#     run.run_engine()
#     return {"response": {"ads": ads, "ratings": run.plugin.interests, "seed": run.seed}}


def clean_input(input):
    for item in input.items():
        input[item[0]] = int(item[1])
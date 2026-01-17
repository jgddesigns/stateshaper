import json
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from src.main.classes.connector.Connector import Connector
from src.main.demos.lesson_plan.lesson_list import lesson_list
from src.main.demos.lesson_plan.LessonPlan import LessonPlan
from src.main.run import RunEngine
from fastapi.middleware.cors import CORSMiddleware
lessons = LessonPlan()

count = 10

app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stateshaper-lessons.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

run = Connector(lessons.sort_ratings())
run.start_connect()


class Input(BaseModel):
    message: str


@app.post("/api/start")
def start():
    lessons.get_data(count)
    run.engine["vocab"] = run.compressed_seed["v"]
    return {"response": {"lesson": run.engine["vocab"], "questions": lessons.current_questions, "ratings": lessons.current_ratings, "seed": [run.compressed_seed, run.engine]}}


@app.post("/api/process")
def process(input: Input):
    input = json.loads(input.message)
    lessons.after_test(input)
    connect = Connector(lessons.data)
    connect.start_connect()
    lessons.get_data(count)
    connect.engine["vocab"] = connect.compressed_seed["v"]    
    return {"response": {"lesson": connect.engine["vocab"], "questions": lessons.current_questions, "ratings": lessons.current_ratings, "seed": [connect.compressed_seed, connect.engine]}}
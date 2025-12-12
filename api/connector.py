# import json
# import os
# import sys
# # from fastapi import FastAPI
# # from fastapi.responses import HTMLResponse
# # from pydantic import BaseModel
# # from fastapi.middleware.cors import CORSMiddleware

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), "src/main"))

# from classes.connector.Connector import Connector
# from run import RunEngine

# # app = FastAPI(
# #     title="Vercel + FastAPI",
# #     description="Vercel + FastAPI",
# #     version="1.0.0",
# # )

# run = RunEngine()


# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )


# # class Input(BaseModel):
# #     message: str

# from typing import Any, Dict

# def handler(request) -> Dict[str, Any]:
#     return {"hello": "world"}


# # @app.post("/api/start")
# # def start():
# #     ads = run.plugin.get_data()
# #     run.connector = Connector(ads)
# #     run.run_engine()
# #     return {"response": {"ads": ads, "ratings": run.plugin.interests, "seed": run.seed}}


# # @app.post("/api/process")
# # def process(input: Input):
# #     input = json.loads(input.message)
# #     clean_input(input)
# #     new_data = run.plugin.change_data(input)
# #     run.connector = Connector(new_data)
# #     run.run_engine()
# #     return {"response": {"ads": new_data, "ratings": run.plugin.interests, "seed": run.seed}}


# def clean_input(input):
#     for item in input.items():
#         input[item[0]] = int(item[1])

import json
import os
import sys

# Make sure paths are available
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "src/main"))

from classes.connector.Connector import Connector
from run import RunEngine


run = RunEngine()


def clean_input(data):
    for key, value in data.items():
        data[key] = int(value)


def handler(request):
    """
    Vercel Python serverless entry point.
    This replaces Flask, FastAPI, and uvicorn.
    """
    return {"hello": "world"}
    # path = request.path or ""
    # method = request.method

    # # Read JSON body (Vercel built-in)
    # try:
    #     body = request.json() or {}
    # except Exception:
    #     body = {}

    # # ---------- ROUTE: /api/start ----------
    # if path.endswith("/start"):
    #     ads = run.plugin.get_data()
    #     run.connector = Connector(ads)
    #     run.run_engine()

    #     return {
    #         "response": {
    #             "ads": ads,
    #             "ratings": run.plugin.interests,
    #             "seed": run.seed
    #         }
    #     }

    # # ---------- ROUTE: /api/process ----------
    # if path.endswith("/process"):
    #     if "message" in body:
    #         input_data = json.loads(body["message"])
    #     else:
    #         input_data = body

    #     clean_input(input_data)

    #     new_data = run.plugin.change_data(input_data)
    #     run.connector = Connector(new_data)
    #     run.run_engine()

    #     return {
    #         "response": {
    #             "ads": new_data,
    #             "ratings": run.plugin.interests,
    #             "seed": run.seed
    #         }
    #     }

    # # ---------- DEFAULT ----------
    # return {
    #     "error": "Route not found",
    #     "path": path
    # }

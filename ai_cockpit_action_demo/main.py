from __future__ import annotations
import threading
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.responses import Response

import os

from models import Action
from models import Config
from models import Mode

from executor import Executor
from raspi_executor.raspi_executor import Raspi_Executor

config = Config()
config.contextPathBase = os.environ.get('CONTEXT_PATH', '/executor')
config.mode = os.environ.get('MODE', Mode.EMULATED)
config.minimum_execution_time = os.environ.get('MINIMUM_EXECUTION_TIME', 5)
config.service_uri = os.environ.get('SERVICE_URI', 'http://localhost:8000')
config.print()

match config.mode:
    case "EMULATED":
        executor = Executor()
        executor.config(config)
    case "RASPI":
        executor = Raspi_Executor()
        executor.config(config)
    case _:
        print("Could not choose executor type")

app = FastAPI(
    title='Executor Service',
    version='0.0.1',
    description='This service provides executions for actions and status for results.\n',
    servers=[{'url': config.service_uri}],
)

scheduler = BackgroundScheduler()

@app.get(config.contextPathBase + '/action', response_model=List[Action], description="Lists all available actions")
def list_action() -> List[Action]:
    executor.check_if_finished()
    return executor.actions

@app.get(config.contextPathBase + '/action/{id}', description="Triggers a new execution for action, false if action is still executing")
def execute_action(id) -> bool:
    return executor.execute_action(id)

@app.get(config.contextPathBase + "/healthcheck")
async def healthcheck():
    return Response()

@app.on_event("startup")
def startup_event():
    scheduler.add_job(do_work, "interval", seconds=5)
    scheduler.start()

def do_work():
    print("roll the dice to finish executions...")
    executor.check_if_finished()
       

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


main()

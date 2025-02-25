from __future__ import annotations
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from models import Mode
from models import Action
from config import Config

from executor import Executor
from raspi_executor.raspi_executor import Raspi_Executor

config = Config()

match config.mode:
    case Mode.EMULATED:
        executor = Executor()
    case Mode.RASPI:
        executor = Raspi_Executor()
    case _:
        print("Could not choose executor type - emulated")
        executor = Executor()
executor.config(config)

app = FastAPI(
    title='Executor Service',
    version='0.0.1',
    description='This service provides executions for actions and status for results.\n',
    servers=[{'url': config.service_uri}],
)

app.mount("/panel", StaticFiles(directory="static", html = True), name="static")

# will run in background to finish actions
scheduler = BackgroundScheduler()

@app.get(config.contextPathBase + '/action', response_model=List[Action], description="Lists all available actions")
def list_action() -> List[Action]:
    executor.check_if_finished()
    return executor.actions

@app.get(config.contextPathBase + '/action/{id}', description="Triggers a new execution for action, false if action is still executing")
def execute_action(id) -> bool:
    return executor.execute_action(id)

@app.delete(config.contextPathBase + '/action', response_model=List[Action], description="Stop all executions")
def stop_action() -> List[Action]:
    executor.stop_all()
    return executor.actions

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

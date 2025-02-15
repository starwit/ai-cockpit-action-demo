from __future__ import annotations
from typing import List

from fastapi import FastAPI
from fastapi.responses import Response

import os

from models import Action
from models import Config

import executor

config = Config()

app = FastAPI(
    title='Executor Service',
    version='0.0.1',
    description='This service provides executions for actions and status for results.\n',
    servers=[{'url': 'http://localhost:8000'}],
)

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

def setup_config():
    config.contextPathBase = os.environ.get('CONTEXT_PATH', '/excecutor')
    config.mode = os.environ.get('MODE', 'EMULATED')
    config.minimum_execution_time = os.environ.get('MINIMUM_EXECUTION_TIME', 5)
    config.print()

def main():
    setup_config()
    executor.setup()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


main()

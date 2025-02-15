from __future__ import annotations
from typing import List

from fastapi import FastAPI
from fastapi.responses import Response

from models import Execution
from models import Action

import executor

contextPathBase = "/excecutor"

app = FastAPI(
    title='Executor Service',
    version='0.0.1',
    description='This service provides executions for actions and status for results.\n',
    servers=[{'url': 'http://localhost:8000'}],
)

@app.get(contextPathBase + '/action', response_model=List[Action], description="Lists all available actions")
def list_action() -> List[Action]:
    executor.check_if_finished()
    return executor.actions

@app.get(contextPathBase + '/action/{id}', description="Triggers a new execution for action, false if action is still executing")
def execute_action(id) -> bool:
    return executor.execute_action(id)

@app.get(contextPathBase + "/healthcheck")
async def healthcheck():
    return Response()

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    executor.setup()

main()

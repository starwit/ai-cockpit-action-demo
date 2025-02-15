from __future__ import annotations
from typing import List
from datetime import datetime
import pathlib

from fastapi import FastAPI
from fastapi.responses import Response

from .models import Info
from .models import Execution

app = FastAPI(
    title='Executor Service',
    version='0.0.1',
    description='This service provides executions for actions and status for results.\n',
    servers=[{'url': 'http://localhost:8080/v0'}],
)

contextPathBase = "/excecutor"

@app.get(contextPathBase + '/info', response_model=Info)
def get_info() -> Info:
    info = Info()
    info.generation_date = datetime.now()
    info.systemDescription = "Action Executor"
    info.apiVersion = "0.0.1"
    return info

@app.get(contextPathBase + '/action/{type}/{id}')
def execute_action() -> str:
    return "true"

@app.get(contextPathBase + '/action/status', response_model=List[Execution])
def execute_action() -> List[Execution]:
    return "true"

@app.get(contextPathBase + "/healthcheck")
async def healthcheck():
    return Response()

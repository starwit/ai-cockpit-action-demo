# generated by fastapi-codegen:
#   filename:  api-definition/logoservice.yaml
#   timestamp: 2024-06-20T18:48:54+00:00

from __future__ import annotations
from enum import Enum

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing import List

class Mode(Enum):
    EMULATED = "EMULATED"
    RASPI = "RASPI"

class Execution_status(Enum):
    EXECUTING = "EXECUTING"
    FINISHED = "FINISHED"

class Config():
    contextPathBase: str = "/executor"
    mode: Mode = Mode.EMULATED
    minimum_execution_time: int = 5

    def print(self):
        print("contextPathBase: " + self.contextPathBase)
        print("mode: " + self.mode)
        print("minimum_execution_time: " + str(self.minimum_execution_time))

class Action(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    executions: Optional[List[Execution]] = None

class Execution(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[Execution_status] = None
    triggeredAt: Optional[datetime] = None
    finishedAt: Optional[datetime] = None
from __future__ import annotations
from enum import Enum

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing import List

class Mode(str, Enum):
    EMULATED = "EMULATED"
    RASPI = "RASPI"

class Execution_status(Enum):
    EXECUTING = "EXECUTING"
    FINISHED = "FINISHED"

class Config():
    service_uri = "http://localhost:8000"
    contextPathBase: str = "/executor"
    mode: Mode = Mode.EMULATED
    minimum_execution_time: int = 5

    def print(self):
        print("service uri " + self.service_uri)
        print("contextPathBase: " + self.contextPathBase)
        print("mode: " + str(self.mode))
        print("minimum_execution_time: " + str(self.minimum_execution_time))

class Action(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    executions: Optional[List[Execution]] = None
    
class HardwareAction(Action):
    iopin: int = None

class Execution(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[Execution_status] = None
    triggeredAt: Optional[datetime] = None
    finishedAt: Optional[datetime] = None
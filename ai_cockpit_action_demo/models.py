from __future__ import annotations
from enum import Enum

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from typing import List

class Mode(str, Enum):
    EMULATED = "EMULATED"
    RASPI = "RASPI"

class Execution_status(Enum):
    EXECUTING = "EXECUTING"
    FINISHED = "FINISHED"

class Action(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    iopin: int = None
    executions: Optional[List[Execution]] = None

class Execution(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[Execution_status] = None
    triggeredAt: Optional[datetime] = None
    finishedAt: Optional[datetime] = None
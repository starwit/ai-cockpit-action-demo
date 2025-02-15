from pydantic import BaseModel
from typing import Dict
from models import Action

class RaspiConfig(BaseModel):
    action_gpio: Dict[Action, int] = None
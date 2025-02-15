
from datetime import datetime
from models import Execution
from models import Execution_status
from models import Action
import random

actions = [
    Action(id=1, name="Police patrol 01", description="Send police crew to investigate"),
    Action(id=2, name="Police patrol 01", description="Send police crew to investigate"),
    Action(id=3, name="Firefighters", description="Dispatch firefighters"),
    Action(id=4, name="Tow service", description="Dispatch tow service, to remove disabled vehicles"),
    Action(id=5, name="Medic team", description="Dispatch medic first responders"),
    Action(id=6, name="Broad cast message", description="Send broad cast message to inform citizens"),
    Action(id=7, name="Send V2X message", description="Send V2X message to proliferate data to automatic/semi-automatic vehicles")
]

minimum_execution_time = 5

def setup():
    for action in actions:
        action.executions = []

def execute_action(id):
    action = actions[int(id)]
    # check if an action is already running
    if not action.executions:
        # no action, create a new one
        action.executions = []
        execution = Execution()
        execution.id = 1
        execution.name = action.name
        execution.status = Execution_status.EXECUTING
        execution.triggeredAt = datetime.now()
        action.executions.append(execution)
        return True
    else:
        # check if the action is already running
        execution = action.executions[-1]
        if execution.status == Execution_status.EXECUTING:
            # action is already running, random choice, to finish
            runtime = datetime.now() - execution.triggeredAt
            print("runtime: " + str(runtime))
            if runtime.total_seconds() > minimum_execution_time and bool(random.getrandbits(1)):
                # action is finished
                execution.status = Execution_status.FINISHED
                execution.finishedAt = datetime.now()
                # create a new execution
                execution = Execution()
                execution.id = len(action.executions) + 1
                execution.name = action.name
                execution.status = Execution_status.EXECUTING
                execution.triggeredAt = datetime.now()
                action.executions.append(execution)
                return True
            return False
        else:
            # action is not running, create a new one
            execution = Execution()
            execution.id = len(action.executions) + 1
            execution.name = action.name
            execution.status = Execution_status.EXECUTING
            execution.triggeredAt = datetime.now()
            action.executions.append(execution)
            return True
    
def check_if_finished():
    for action in actions:
        if action.executions:
            execution = action.executions[-1]
            if execution.status == Execution_status.EXECUTING:
                runtime = datetime.now() - execution.triggeredAt
                if runtime.total_seconds() > minimum_execution_time and bool(random.getrandbits(1)):
                    # action is finished
                    execution.status = Execution_status.FINISHED
                    execution.finishedAt = datetime.now()
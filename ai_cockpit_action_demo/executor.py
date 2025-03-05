from __future__ import annotations
from typing import Optional
from datetime import datetime
import random
import json

from models import Execution
from models import Execution_status
from models import Action
from config import Config

class Executor:
    config: Config = None

    actions = [
        Action(id=1, name="Police patrol 01", description="Send police crew to investigate"),
        Action(id=2, name="Police patrol 01", description="Send police crew to investigate"),
        Action(id=3, name="Firefighters", description="Dispatch firefighters"),
        Action(id=4, name="Tow service", description="Dispatch tow service, to remove disabled vehicles"),
        Action(id=5, name="Medic team", description="Dispatch medic first responders"),
        Action(id=6, name="Broad cast message", description="Send broad cast message to inform citizens"),
        Action(id=7, name="Send V2X message", description="Send V2X message to proliferate data to automatic/semi-automatic vehicles"),
        Action(id=8, name="Stop Traffic", description="Reschedule traffic lights, to stop traffic from flowing into a certain area.")
    ]
       
    def __init__(self):
        for action in self.actions:
            action.executions = []
            
    def set_config(self, config):
        self.config = config
        self.import_action_mapping()
        
        
    def stop_action(self, id):
        action = self.actions[int(id)-1]
        if action.executions:
            execution = action.executions[-1]
            if execution.status == Execution_status.EXECUTING:
                execution.status = Execution_status.FINISHED
                execution.finishedAt = datetime.now()
                self.deactivate(action)

        return action
    
    def stop_all(self):
        print("Stopping all executions")
        for action in self.actions:
            if action.executions:
                execution = action.executions[-1]
                if execution.status == Execution_status.EXECUTING:
                    execution.status = Execution_status.FINISHED
                    execution.finishedAt = datetime.now()
                    self.deactivate(action)

    def execute_action(self, id):
        action = self.actions[int(id)-1]
        # check if an action is already running
        if not action.executions:
            # no action, create a new one
            print("Create new execution for action " + action.name)
            action.executions = []
            execution = Execution()
            execution.id = 1
            execution.name = action.name
            execution.status = Execution_status.EXECUTING
            execution.triggeredAt = datetime.now()
            self.activate(action)
            action.executions.append(execution)
            return True
        else:
            # check if the action is already running
            execution = action.executions[-1]
            if execution.status == Execution_status.EXECUTING:
                # action is already running
                return False
            else:
                # action is not running, create a new one
                execution = Execution()
                execution.id = len(action.executions) + 1
                execution.name = action.name
                execution.status = Execution_status.EXECUTING
                execution.triggeredAt = datetime.now()
                self.activate(action)
                action.executions.append(execution)
                return True
        
    def check_if_finished(self):
        for action in self.actions:
            if action.executions:
                execution = action.executions[-1]
                if execution.status == Execution_status.EXECUTING:
                    runtime = datetime.now() - execution.triggeredAt
                    if runtime.total_seconds() > self.config.minimum_execution_time and bool(random.getrandbits(1)):
                        # action is finished
                        execution.status = Execution_status.FINISHED
                        execution.finishedAt = datetime.now()
                        self.deactivate(action)
                        
    def activate(self, action):
        pass
        
    def deactivate(self, action):
        pass
    
    def get_action(self, id):
        return self.actions[int(id)-1]
    
    def import_action_mapping(self):
        print("Import action mapping from " + self.config.mapping_import_file)
        f = open(self.config.mapping_import_file)
        data = json.load(f)
        self.actions = []
        for action in data:
            self.actions.append(Action(id=action["id"], iopin=action["iopin"], name=action["name"], description=action["description"], executions=[]))
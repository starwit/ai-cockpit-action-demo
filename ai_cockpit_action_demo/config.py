from enum import Enum
import os

from models import Mode

class Config():
    service_uri = "http://localhost:8000"
    contextPathBase: str = "/executor"
    mode: Mode = Mode.EMULATED
    minimum_execution_time: int = 5
    
    def __init__(self):
        self.contextPathBase = os.environ.get('CONTEXT_PATH', '/executor')
        self.minimum_execution_time = os.environ.get('MINIMUM_EXECUTION_TIME', 5)
        self.service_uri = os.environ.get('SERVICE_URI', 'http://localhost:8000')
        self.print()    
        
        print("Test if GPIO device is present")
        if(os.path.exists("/dev/gpiochip0")):
            print("GPIO hardware appears to be present -> MODE=RASPI")
            self.mode = "RASPI"
        else:
            self.mode = os.environ.get('MODE', Mode.EMULATED)

    def print(self):
        print("service uri " + self.service_uri)
        print("contextPathBase: " + self.contextPathBase)
        print("mode: " + str(self.mode))
        print("minimum_execution_time: " + str(self.minimum_execution_time))
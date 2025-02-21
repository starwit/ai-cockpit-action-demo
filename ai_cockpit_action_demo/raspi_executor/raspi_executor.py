from models import HardwareAction
from executor import Executor
import lgpio

class Raspi_Executor(Executor):
    actions = [
        HardwareAction(id=1, iopin=5, name="Police patrol 01", description="Send police crew to investigate"),
        HardwareAction(id=2, iopin=6, name="Police patrol 01", description="Send police crew to investigate"),
        HardwareAction(id=3, iopin=13, name="Firefighters", description="Dispatch firefighters"),
        HardwareAction(id=4, iopin=17, name="Tow service", description="Dispatch tow service, to remove disabled vehicles"),
        HardwareAction(id=5, iopin=22, name="Medic team", description="Dispatch medic first responders"),
        HardwareAction(id=6, iopin=23, name="Broad cast message", description="Send broad cast message to inform citizens"),
        HardwareAction(id=7, iopin=24, name="Send V2X message", description="Send V2X message to proliferate data to automatic/semi-automatic vehicles"),
        HardwareAction(id=8, iopin=27, name="Stop Traffic", description="Reschedule traffic lights, to stop traffic from flowing into a certain area.")
    ]
    
    handle = None # GPIO handle
    gpio_chip = 0  # Typically 0 for Raspberry Pi
    
    def __init__(self):
        super().__init__()
        self.handle = lgpio.gpiochip_open(self.gpio_chip)
        print("switching all outputs to zero")
        for action in self.actions:
            lgpio.gpio_claim_output(self.handle, action.iopin)
            print("switching output " + str(action.iopin) + " to zero")
            lgpio.gpio_write(self.handle, action.iopin, 0)           
    
    def activate(self, action):
        print("switching output " + str(action.iopin) + " to ON")
        lgpio.gpio_write(self.handle, action.iopin, 1)
        
    def deactivate(self, action):
        print("switching output " + str(action.iopin) + " to OFF")
        lgpio.gpio_write(self.handle, action.iopin, 0)
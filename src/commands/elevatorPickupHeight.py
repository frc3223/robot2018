import wpilib.command
import ctre

class elevatorPickupHeight(wpilib.command.Command):
    def __init__(self):
        super().__init__("elevatorPickupHeight")
        #Add finishing stuff that will have the motors and controls for the controller. This will be for button A!
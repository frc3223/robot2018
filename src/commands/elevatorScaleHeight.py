import wpilib.command
import ctre

class elevatorScaleHeight(wpilib.command.Command):
    def __init__(self):
        super().__init__("elevatorScaleHeight")
        #Add finishing stuff that will have the motors and controls for the controller. This will be for button Y!
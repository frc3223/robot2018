import wpilib.command
import ctre

class elevatorDownHeight(wpilib.command.Command):
    def __init__(self):
        super().__init__("elevatorDownHeight")
        #Add finishing stuff that will have the motors and controls for the controller. This will be for button X!
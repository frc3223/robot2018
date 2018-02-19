import wpilib.command
from oi import getJoystick

class Grabber(wpilib.command.Command):
    def __init__(self):
        super().__init__("Grabber")
        self.intake = self.getRobot().intake
        self.requires(self.intake)


    def execute(self):
        joystick = getJoystick()
        closeArm_trigger = joystick.getRawAxis(3) #Right Trigger
        openArm_trigger = joystick.getRawAxis(2) #Left Trigger
        if closeArm_trigger < 0: # right trigger triggered
            self.intake.closeGrabber()
        elif openArm_trigger < 0: #left trigger triggered
            self.intake.openGrabber()
        else:
            self.intake.grabberOff()
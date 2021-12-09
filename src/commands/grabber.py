import wpilib.command
from oi import getJoystick
from oi import getJoystick1

class Grabber(wpilib.command.Command):
    def __init__(self):
        super().__init__("Grabber")
        self.intake = self.getRobot().intake
        self.requires(self.intake)


    def execute(self):
        joystick = getJoystick()
        joystick1 = getJoystick1()
        turnOffWheels = True
        closeArm_trigger = joystick1.getRawAxis(3) #Right Trigger
        openArm_trigger = joystick1.getRawAxis(2) #Left Trigger
        if abs(closeArm_trigger) > 0.1: # right trigger triggered
            self.intake.closeGrabber(closeArm_trigger)
        elif abs(openArm_trigger) > 0.1: #left trigger triggered
            self.intake.openGrabber()
        elif joystick1.getRawButton(3):
            self.intake.open2Grabber()
        elif joystick1.getRawButton(2):
            self.intake.open2Grabber()
            turnOffWheels = False
        else:
            self.intake.grabberOff()

        if joystick1.getRawButton(5):
            self.intake.cubeOut()
        elif joystick1.getRawButton(6):
            self.intake.cubeIn()
        elif turnOffWheels:
            self.intake.intakeWheelsOff()
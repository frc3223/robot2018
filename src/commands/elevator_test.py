from wpilib.command import Command
from oi import getJoystick
from oi import getJoystick1
import wpilib

class ElevatorTest(Command):
    def __init__(self):
        super().__init__('ElevatorTest')
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)
        self.joystick1 = getJoystick1()


    def execute(self):
        isDisabled = wpilib.DriverStation.getInstance().isDisabled()
        if self.joystick1.getPOV(0) == 0: #Up on D-pad pressed
            self.elevator.test_drive_positive()
        elif self.joystick1.getPOV(0) == 180: #Down on D-pad pressed
            self.elevator.test_drive_negative()
        elif isDisabled:
            self.elevator.off()
        else:
            self.elevator.hover()


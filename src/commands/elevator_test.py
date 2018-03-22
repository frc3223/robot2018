from wpilib.command import Command
from oi import getJoystick
import wpilib

class ElevatorTest(Command):
    def __init__(self):
        super().__init__('ElevatorTest')
        self.elevator = self.getRobot().elevator
        self.joystick = getJoystick()
        self.requires(self.elevator)


    def execute(self):
        isDisabled = wpilib.DriverStation.getInstance().isDisabled()
        if self.joystick.getPOV(0) == 0: #Up on D-pad pressed
            self.elevator.test_drive_positive()
        elif self.joystick.getPOV(0) == 180: #Down on D-pad pressed
            self.elevator.test_drive_negative()
        elif isDisabled:
            self.elevator.off()
        else:
            self.elevator.hover()


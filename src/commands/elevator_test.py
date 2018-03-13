from wpilib.command import Command
from oi import getJoystick

class ElevatorTest(Command):
    def __init__(self):
        super().__init__('ElevatorTest')
        self.elevator = self.getRobot().elevator
        self.joystick = getJoystick()
        self.requires(self.elevator)

    def execute(self):
        if self.joystick.getPOV(0) == 0: #Up on D-pad pressed
            self.elevator.test_drive_positive()
        elif self.joystick.getPOV(0) == 180: #Down on D-pad pressed
            self.elevator.test_drive_negative()
        else:
            self.elevator.hover()

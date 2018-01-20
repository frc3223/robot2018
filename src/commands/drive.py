import wpilib.command
from oi import getJoystick

class Drive(wpilib.command.Command):
    def __init__(self):
        super().__init__('Drive')
        self.requires(self.getRobot().drivetrain)

    def execute(self):
        joystick = getJoystick()
        self.getRobot().drivetrain.drive(joystick)

    def isFinished(self):
        return False
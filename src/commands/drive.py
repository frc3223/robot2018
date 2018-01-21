import wpilib.command
from oi import getJoystick

class Drive(wpilib.command.Command):
    def __init__(self):
        super().__init__('Drive')
        self.requires(self.getRobot().drivetrain)

    def execute(self):
        joystick = getJoystick()
        fw = joystick.getRawAxis(1)
        lr = joystick.getRawAxis(4)
        self.getRobot().drivetrain.drive.arcadeDrive(fw, lr)

    def isFinished(self):
        return False

import wpilib.command
from oi import getJoystick

class Drive(wpilib.command.Command):
    def __init__(self):
        super().__init__('Drive')
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)

    def execute(self):
        self.drivetrain.mode = "Drive"
        joystick = getJoystick()
        fw = joystick.getRawAxis(1)
        lr = joystick.getRawAxis(4)
        self.drivetrain.drive.arcadeDrive(fw, lr)

    def isFinished(self):
        return False

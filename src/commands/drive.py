import wpilib.command
from oi import getJoystick

class Drive(wpilib.command.Command):
    def __init__(self):
        super().__init__('Drive')
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)

    def initialize(self):
        self.drivetrain.motor_lb.configOpenLoopRamp(0.2, 0)
        self.drivetrain.motor_rb.configOpenLoopRamp(0.2, 0)

    def execute(self):
         self.drivetrain.mode = "Drive"
         joystick = getJoystick()
         fw = joystick.getRawAxis(1)
         lr = joystick.getRawAxis(0)
         self.drivetrain.drive.arcadeDrive(fw*.75, lr*.75)
        #self.janky()


    def isFinished(self):
        return False
    '''
    def janky(self):
        self.drivetrain.mode = "Drive"
        joystick = getJoystick()
        if joystick.getPOV(0) == 90:
            self.drivetrain.motor_rb.set(0.40)
            self.drivetrain.motor_lb.set(0.40)
        elif joystick.getPOV(0) == 270:
                self.drivetrain.motor_rb.set(-0.40)
                self.drivetrain.motor_lb.set(-0.40)
        else:
            self.drivetrain.motor_rb.set(0)
            self.drivetrain.motor_lb.set(0)
            '''

import wpilib
import csv
import wpilib.command
from wpilib.buttons.joystickbutton import JoystickButton
from oi import getJoystick
from pidcommand import PIDCommand


class Turntoangle(PIDCommand):
    def __init__(self, setpoint):
        super().__init__(p=.003, i=0.0001, d=0.06, period=.010)

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        pid = self.getPIDController()
        pid.setInputRange(minimumInput=-180, maximumInput=180)
        pid.setOutputRange(minimumOutput=-1, maximumOutput=1)
        self.setSetpoint(setpoint)
        self.logger = None
        self.joystick = getJoystick()
        self.pdp = wpilib.PowerDistributionPanel(16)

    def initialize(self):
        super().initialize()

        self.timer = wpilib.Timer()
        self.timer.start()

        self.drivetrain.motor_rb.configClosedLoopRamp(2, 0)
        self.drivetrain.motor_lb.configClosedLoopRamp(2, 0)

        filepath = '/home/lvuser/turn.csv'
        if wpilib.RobotBase.isSimulation():
            filepath = './turn.csv'
        self.logger = csv.writer(open(filepath, 'w'))
        self.logger.writerow(["time", "heading", "output", "buttonpressed", "preleftmotor", "prerightmotor", "postrightmotor", "postleftmotor", "talon0", "talonc1", "talonc2", "talon14", "talon15"])

    def returnPIDInput(self):
        return self.drivetrain.navx.getYaw()

    def usePIDOutput(self, output):
        t = self.timer.get()
        b = self.joystick.getRawButton(5)
        l = self.drivetrain.motor_lb.get()
        r = self.drivetrain.motor_rb.get()
        if self.logger is not None:
           self.drivetrain.mode = "Turn"
        self.drivetrain.drive.arcadeDrive(0, output)
        lp = self.drivetrain.motor_lb.get()
        rp = self.drivetrain.motor_rb.get()
        z = self.pdp.getCurrent(0)
        x = self.pdp.getCurrent(1)
        c = self.pdp.getCurrent(14)
        v = self.pdp.getCurrent(15)



        self.logger.writerow([t, self.returnPIDInput(), output, b, l , r, lp, rp, z, x, c, v])




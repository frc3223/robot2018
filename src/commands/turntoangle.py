import wpilib
import csv
import wpilib.command


class Turntoangle(wpilib.command.PIDCommand):
    def __init__(self, setpoint):
        super().__init__(p=.003, i=0.0001, d=0.06, period=.010)

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        pid = self.getPIDController()
        pid.setInputRange(minimumInput=-180, maximumInput=180)
        pid.setOutputRange(minimumOutput=-1, maximumOutput=1)
        self.setSetpoint(setpoint)
        self.logger = None

    def initialize(self):
        super().initialize()

        self.timer = wpilib.Timer()
        self.timer.start()

        filepath = '/home/lvuser/turn.csv'
        if wpilib.RobotBase.isSimulation():
            filepath = './turn.csv'
        self.logger = csv.writer(open(filepath, 'w'))
        self.logger.writerow(["time", "heading", "output"])

    def returnPIDInput(self):
        return self.drivetrain.navx.getYaw()

    def usePIDOutput(self, output):
        t = self.timer.get()
        if self.logger is not None:
            self.logger.writerow([t, self.returnPIDInput(), output])
        self.drivetrain.mode = "Turn"
        self.drivetrain.drive.arcadeDrive(0, output)




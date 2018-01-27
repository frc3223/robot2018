import wpilib
import wpilib.command


class Turntoangle(wpilib.command.PIDCommand):
    def __init__(self, setpoint):
        super().__init__(p=.1, i=0, d=0, period=.010)

        self.requires(self.getRobot().drivetrain)
        pid = self.getPIDController()
        pid.setInputRange(minimumInput=0, maximumInput=360)
        pid.setOutputRange(minimumOutput=-1, maximumOutput=1)
        self.setSetpoint(setpoint)
    def returnPIDInput(self):
        return self.getRobot().drivetrain.navx.getAngle()

    def usePIDOutput(self, output):
        self.getRobot().drivetrain.drive.arcadeDrive(0, output)




import wpilib.command
import ctre

class grabberPullIn(wpilib.command.Command):
    def __init__(self):
        super().__init__("grabberPullIn")
        self.intake = self.getRobot().intake
        self.requires(self.intake)

    def execute(self):
        #set both wheel motors to full reverse speed
        self.intake.motor_leftWheel_set(-1)
        self.intake.motor_rightWheel_set(-1)
import wpilib.command
import ctre

class grabberSpitOut(wpilib.command.Command):
    def __init__(self):
        super().__init__("grabberSpitOut")
        self.intake = self.getRobot().intake
        self.requires(self.intake)

    def execute(self):
        #set both motors to full forward speed
        self.intake.motor_leftWheel_set(1)
        self.intake.motor_rightWheel_set(1)


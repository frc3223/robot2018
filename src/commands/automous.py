import wpilib
import ctre
import wpilib.command
import commands
from commands import driveForward
from subsystems import drivetrain


class Test(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("automous")
        self.addSequential(driveForward.DriveForward(10))
        self.addSequential(driveForward.DriveForward(-2))
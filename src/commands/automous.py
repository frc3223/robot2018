import wpilib
import ctre
import wpilib.command
import commands
from commands import driveForward
from subsystems import drivetrain
from commands import autoEncoders
import time


class SequentialCommands(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("automous")
        self.drivetrain = self.getRobot().drivetrain
        self.addSequential(commands.autoEncoders.AutoEncoders(10))
        self.addSequential(commands.autoEncoders.AutoEncodersTurnLeft(90))
        self.addSequential(commands.autoEncoders.AutoEncodersTurnRight(90))
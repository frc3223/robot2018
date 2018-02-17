import ctre
import wpilib.command
import commands
from commands import driveForward
from subsystems import drivetrain


class gotoScale(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("gotoSwitch")
        self.elevatorZero = self.getRobot().elevatorZero
        self.gamecode = self.getRobot().gamecode[[1:] #get first team switch character via substrings

    def initialize(self):
        pass

    def execute(self):
        AddPararell(self.elevatorZero)
        if self.gamecode == "l" #L the Letter
            AddSequential(driveForward.DriveForward(14)) #move x feet
            AddSequential(turn_profiled.TurnProfiled(90)) #turn x degrees
        else:
            AddSequential(driveForward.DriveForward(10)) #move x feet
            AddSequential(turn_profiled.TurnProfiled(90)) #turn x degrees
            AddSequential(driveForward.DriveForward(20))
            AddSequential(turn_profiled.TurnProfiled(-90))
            AddSequential(driveForward.DriveForward(4))
            AddSequential(turn_profiled.TurnProfiled(-90))




    def end(self):
        pass

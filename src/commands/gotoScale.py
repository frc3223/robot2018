import ctre
import wpilib.command
import commands
from commands import driveForward
from subsystems import drivetrain


class gotoScale(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("gotoScale")
        self.elevatorZero = self.getRobot().elevatorZero
        self.gamecode = self.getRobot().gamecode[2:][:1] #get middle scale character via substrings

    def initialize(self):
        pass

    def execute(self):
        AddPararell(self.elevatorZero)
        if self.gamecode == "l" #L the Letter
            AddSequential(driveForward.DriveForward(27)) #move x feet
            AddSequential(turn_profiled.TurnProfiled(90)) #turn x degrees
        else:
            AddSequential(driveForward.DriveForward(18)) #move x feet
            AddSequential(turn_profiled.TurnProfiled(90)) #turn x degrees
            AddSequential(driveForward.DriveForward(23))
            AddSequential(turn_profiled.TurnProfiled(-90))
            AddSequential(driveForward.DriveForward(9))
            AddSequential(turn_profiled.TurnProfiled(-90))




    def end(self):
        pass

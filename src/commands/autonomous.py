import wpilib.command
import commands
from commands.autoEncoders import *
from commands.autoTimeBased import TimeBasedForward
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, TimeBasedGrabber


class SequentialCommands(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("automous")
        self.drivetrain = self.getRobot().drivetrain
        self.addSequential(commands.autoEncoders.AutoEncoders(13))
        self.addSequential(commands.autoEncoders.AutoEncodersTurnLeft(90))
        #self.addSequential(commands.autoEncoders.AutoEncodersTurnRight(90))


class SwitchCommands(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("Switchy")
        self.addSequential(Parallel(WaitForGamecode(), WaitForAutoIn()))
        self.addSequential(
            IfIsMiddlePosRightSwitch(
                MiddlePosRightSwitchAuto(),
                IfIsRightPosRightSwitch(
                    RightPosRightSwitchAuto(),
                    IfIsLeftPosLeftSwitch(
                        LeftPosLeftSwitchAuto(),
                        Parallel(TimeBasedForward(4), TimeBasedElevator(2))
                    )
                )))


class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            TimeBasedForward(4),
            ElevatorSwitch(),

        ))
        self.addSequential(TimeBasedGrabber(0.5))


class RightPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(TimeBasedForward(1))
        self.addSequential(TimeBasedGrabber(0.5))


class LeftPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(TimeBasedForward(1))
        self.addSequential(TimeBasedGrabber(0.5))

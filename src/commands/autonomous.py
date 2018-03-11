import wpilib.command
import commands
from commands import autoEncoders
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, TimeBasedGrabber


class SequentialCommands(wpilib.command.CommandGroup):

    def __init__(self):
        super().__init__("automous")
        self.drivetrain = self.getRobot().drivetrain
        self.addSequential(commands.autoEncoders.AutoEncoders(10))
        self.addSequential(commands.autoEncoders.AutoEncodersTurnLeft(90))
        self.addSequential(commands.autoEncoders.AutoEncodersTurnRight(90))


class SwitchCommands(wpilib.command.CommandGroup):
    def __init__(self):
        self.addSequential(Parallel(WaitForGamecode(), WaitForAutoIn()))
        self.addSequential(MiddlePosRightSwitchAuto())
        '''
        self.addSequential(IfIsMiddlePosRightSwitch(
            MiddlePosRightSwitchAuto(),
            IfIsRightPosRightSwitch(
                RightPosRightSwitchAuto(),
                IfIsLeftPosLeftSwitch(
                    LeftPosLeftSwitchAuto(),
                    ForwardOnlyAuto()
                )
            )
        ))'''


class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            commands.autoEncoders.AutoEncoders(10),
            TimeBasedElevator(2),
        ))
        self.addSequential(TimeBasedGrabber(0.5))

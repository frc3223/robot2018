import wpilib.command
import commands
from commands.autoEncoders import *
from commands.autoTimeBased import TimeBasedForward
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, TimeBasedGrabber
from commands.autoNavx import TurnLeft,TurnRight



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
        #self.addSequential(Parallel(WaitForGamecode(), WaitForAutoIn()))
        #self.addSequential(Parallel(AutoEncoders(10), ElevatorSwitch()))
        #

        self.addSequential(Parallel(AutoEncoders(10), ElevatorSwitch()))
        # self.addSequential(WaitForGamecode())
        #
        # self.addSequential(
        #     IfIsMiddlePosRightSwitch(
        #         MiddlePosRightSwitchAuto(),
        #         Parallel(AutoEncoders(10), ElevatorSwitch())))
        '''
        self.addSequential(
            IfIsMiddlePosRightSwitch(
                MiddlePosRightSwitchAuto(),
                    IfIsMiddlePosLeftSwitch(
                        MiddlePosLeftSwitchAuto(),
                IfIsRightPosRightSwitch(
                    RightPosRightSwitchAuto(),
                        IfIsRightPosLeftSwitch(
                            RightPosLeftSwitchAuto(),
                            IfIsLeftPosLeftSwitch(
                            LeftPosLeftSwitchAuto(),
                                IfIsLeftPosRightSwitch(
                                    LeftPosRightSwitchAuto(),

                        Parallel(TimeBasedForward(4), TimeBasedElevator(2))
                    )
                ))))))'''


class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(10.5),
            ElevatorSwitch(),
        ))
        self.addSequential(TimeBasedGrabber(3.0))

class MiddlePosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            #TimeBasedForward(4),
            ElevatorSwitch(),
            Sequential(
                AutoEncoders(6),
                AutoEncodersTurnLeft(90),
                AutoEncoders(10),
                AutoEncodersTurnRight(90),
                AutoEncoders(3),
            )))
        self.addSequential(TimeBasedGrabber(3.0))

class RightPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(14),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(TimeBasedGrabber(3.0))

class RightPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(14),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(13))
        self.addSequential(TimeBasedGrabber(3.0))

class LeftPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(16),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(14))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(1))
        self.addSequential(TimeBasedGrabber(3.0))



class LeftPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(14),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(TimeBasedGrabber(3.0))

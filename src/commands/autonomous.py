import wpilib.command
import commands
from commands.autoEncoders import *
from commands.autoTimeBased import TimeBasedForward
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, TimeBasedGrabber
from commands.autoNavx import turnLeft,turnRight



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
                ))))))


class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(WaitForGamecode(), WaitForAutoIn()))
        self.addSequential(Parallel(
            AutoEncoders(11),
            ElevatorSwitch(),
        ))
        self.addSequential(TimeBasedGrabber(0.5))

class MiddlePosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            #TimeBasedForward(4),
            ElevatorSwitch(),
            Sequential(
                AutoEncoders(3),
                AutoEncodersTurnLeft(90),
                AutoEncoders(10),
                AutoEncodersTurnRight(90),
                AutoEncoders(8.5),
            )))
        self.addSequential(TimeBasedGrabber(0.5))

class RightPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(TimeBasedForward(.5))
        self.addSequential(TimeBasedGrabber(0.5))

class RightPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(18),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(AutoEncoders())
        self.addSequential(TimeBasedGrabber(0.5))

class LeftPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(turnLeft(90))
        self.addSequential(TimeBasedForward(1))
        self.addSequential(TimeBasedGrabber(0.5))



class LeftPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(turnRight(90))
        self.addSequential(TimeBasedForward(1))
        self.addSequential(TimeBasedGrabber(0.5))

import wpilib.command
import commands
from commands.autoEncoders import *
from commands.autoTimeBased import TimeBasedForward
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, SpitOut
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
        self.addSequential(Parallel(WaitForGamecode(), WaitForAutoIn()))

        self.addSequential(
            IfIsMiddlePosRightSwitch(
                MiddlePosRightSwitchAuto(),
                    IfIsMiddlePosLeftSwitch(
                        MiddlePosLeftSwitchAuto(),
                        IfIsRightPosRightSwitch(
                            RightPosRightSwitchAuto(),
                                IfIsRightPosLeftSwitch(
                                    ForwardOnly(),
                                    IfIsLeftPosLeftSwitch(
                                        LeftPosLeftSwitchAuto(),
                                        IfIsLeftPosRightSwitch(
                                            ForwardOnly(),
                                            ForwardOnly()
                            )
                        ))))))

class MiddleOnly(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("Middle only ")
        self.addSequential(WaitForGamecode())
        
        self.addSequential(
            IfIsMiddlePosRightSwitch(
                MiddlePosRightSwitchAuto(),
                MiddlePosLeftSwitchAuto()))
    
class Wait(wpilib.command.Command):
    def __init__(self, time):
        super().__init__("WaitForAutoIn", time)

    def isFinished(self):
        return self.isTimedOut()


class Wait9ThenForward(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("Wait9 then forward")
        self.addSequential(Wait(9))
        self.addSequential(ForwardOnly())

class ForwardOnly(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("Wait9 then forward")
        self.addSequential(Parallel(AutoEncoders(10), ElevatorSwitch()))

class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(10.5),
            ElevatorSwitch(),
        ))
        self.addSequential(SpitOut())

class MiddlePosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            #TimeBasedForward(4),
            ElevatorSwitch(),
            Sequential(
                AutoEncoders(5),
                TurnLeft(90),
                AutoEncoders(9),
                TurnRight(90),
                AutoEncoders(6),
            )))
        self.addSequential(SpitOut())

class RightPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(TurnLeft(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(SpitOut())

class RightPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(14),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(13))
        self.addSequential(SpitOut())

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
        self.addSequential(SpitOut())



class LeftPosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(13),
            ElevatorSwitch(),
        ))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(SpitOut())

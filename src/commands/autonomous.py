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
                                                IfIsRightPosRightScale(
                                                    RightPosRightScaleAuto(),
                                                        IfIsRightPosLeftScale(
                                                            RightPosLeftScaleAuto(),
                                                                IfIsLeftPosLeftScale(
                                                                    LeftPosLeftScaleAuto(),
                                                                        IfIsLeftPosRightScale(
                                                                            LeftPosRightScaleAuto(),
                                                                            ForwardOnly(),
                            )
                        ))))))))))

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
            ElevatorSwitch(),
            Sequential(
                AutoEncoders(5),
                TurnLeft(110),
                AutoEncoders(10.5),
                TurnRight(80),
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
        self.addSequential(TurnLeft(110))
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
        self.addSequential(AutoEncoders(14))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(1))
        self.addSequential(SpitOut())

class LeftPosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(14),
            ElevatorSwitch(),
        ))

        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(AutoEncoders(14))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(3))
        self.addSequential(AutoEncodersTurnLeft(90))
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

class LeftPosLeftScaleAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(22.5),
        ))
        self.addSequential(ElevatorScale())
        self.addSequential(SpitOut())
        self.addSequential(AutoEncoders(-3))
        self.addSequential(ElevatorSwitch(
        ))


class RightPosRightScaleAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(25),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(ElevatorScale())
        self.addSequential(SpitOut())
        self.addSequential(AutoEncoders(-3))
        self.addSequential(ElevatorSwitch())

class LeftPosRightScaleAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(20),
        ))

        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(16.5))
        self.addSequential(AutoEncodersTurnLeft(130))
        self.addSequential(AutoEncoders(6))
        self.addSequential(AutoEncoders(-1))
        self.addSequential(ElevatorScale())
        self.addSequential(SpitOut())
        self.addSequential(AutoEncoders(-3))
        self.addSequential(ElevatorSwitch())



class RightPosLeftScaleAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(Parallel(
            AutoEncoders(20),
        ))

        self.addSequential(AutoEncodersTurnLeft(110))
        self.addSequential(AutoEncoders(16))
        self.addSequential(AutoEncodersTurnRight(90))
        self.addSequential(AutoEncoders(6))
        self.addSequential(AutoEncoders(-1))
        self.addSequential(ElevatorScale())
        self.addSequential(SpitOut())
        self.addSequential(AutoEncoders(-3))
        self.addSequential(ElevatorSwitch())

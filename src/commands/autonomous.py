import wpilib.command
import commands
from commands.autoEncoders import *
from commands.autoTimeBased import TimeBasedForward
from commands.auto_conditions import *
from commands.autoTimeBased import TimeBasedElevator, SpitOut
from commands.autoNavx import TurnLeft,TurnRight
from commands.multiconditionalcommand import MultiConditionalCommand


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

        
class Autonomuscc(MultiConditionalCommand):
    def __init__(self):
        self.table = networktables.NetworkTables.getTable("SmartDashboard")
        super().__init__("Autocc", [
            ("is_middle_right_switch", MiddlePosRightSwitchAuto()),
            ("is_middle_left_switch", MiddlePosLeftSwitchAuto()),
            ("is_left_priority_switch_gotswitch", LeftPosLeftSwitchAuto()),
            ("is_left_priority_switch_gotscale", LeftPosLeftScaleAuto()),
            ("is_left_priority_scale_gotscale", LeftPosLeftScaleAuto()),
            ("is_left_priority_scale_gotswitch", LeftPosLeftSwitchAuto()),
            ("is_left_switch_gotleft", LeftPosLeftSwitchAuto()),
            ("is_left_scale_gotleft", LeftPosLeftScaleAuto()),
            #("is_left_switch_gotright", LeftPosRightSwitchAuto()),
            #("is_left_scale_gotright", LeftPosRightScaleAuto()),
            ("is_right_priority_switch_gotswitch", RightPosRightSwitchAuto()),
            ("is_right_priority_switch_gotscale", RightPosRightScaleAuto()),
            ("is_right_priority_scale_gotscale", RightPosRightScaleAuto()),
            ("is_right_priority_scale_gotswitch", RightPosRightSwitchAuto()),
            ("is_right_switch_gotright", RightPosRightSwitchAuto()),
            ("is_right_scale_only", RightPosRightScaleAuto()),
            #("is_right_switch_gotleft", RightPosLeftSwitchAuto()),
            #("is_right_scale_gotleft", RightPosLeftScaleAuto()),
            ("driveforward", ForwardOnly()),

        ])
    def is_middle_right_switch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "MSwSwSw" and is_right_switch():
            return True

    def is_middle_left_switch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "MSwSwSw" and is_left_switch():
                return True

    def is_left_priority_switch_gotswitch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LSwScDr" and is_left_switch():
            return True

    def is_left_priority_switch_gotscale(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LSwScDr" and is_left_scale():
            return True

    def is_left_priority_scale_gotscale(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LScSwDr" and is_left_scale():
            return True

    def is_left_priority_scale_gotswitch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LScSwDr" and is_left_switch():
            return True

    def is_left_switch_gotleft(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LSwSwSw" and is_left_switch():
            return True

    def is_left_scale_gotleft(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LScScSc" and is_left_scale():
            return True

    def is_left_switch_gotright(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LSwSwSw" and is_right_switch():
            return True

    def is_left_scale_gotright(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "LScScSc" and is_right_scale():
            return True

    def is_right_priority_switch_gotswitch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RSwScDr" and is_right_switch():
            return True

    def is_right_priority_switch_gotscale(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RSwScDr" and is_right_scale():
            return True

    def is_right_priority_scale_gotscale(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RScSwDr" and is_right_scale():
            return True

    def is_right_priority_scale_gotswitch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RScSwDr" and is_right_switch():
            return True

    def is_right_switch_gotright(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RSwSwSw" and is_right_switch():
            return True

    def is_right_scale_only(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RScScSc" and is_right_scale():
            return True

    def is_right_switch_gotleft(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RSwSwSw" and is_right_switch():
            return True

    def is_right_scale_gotleft(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RScScSc" and is_left_scale():
            return True

    def driveforward(self):
        return True

    def is_right_right_switch(self):
        automode = self.table.getString("autonomousMode", None)
        if automode == "RSwSwSw" and is_right_switch():
                return True


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

class ForwardOnly(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("Wait9 then forward")
        self.addSequential(LogCommands("ForwardOnly"))
        self.addSequential(Parallel(AutoEncoders(10), ElevatorSwitch()))

class MiddlePosRightSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(LogCommands("MiddlePosRightSwitchAuto"))
        self.addSequential(Parallel(
            AutoEncoders(10.5),
            ElevatorSwitch(),
        ))
        self.addSequential(SpitOut())

class LogCommands(wpilib.command.Command):
    def __init__(self, logname):
        super().__init__("LogCommands")
        self.logname = logname
        self.table = networktables.NetworkTables.getTable("/Drivetrain")
    def execute(self):
        self.table.putString("Choosen Auto", self.logname)

    def isFinished(self):
        return True


class MiddlePosLeftSwitchAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(LogCommands("MiddlePosLeftSwitchAuto"))
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
        self.addSequential(LogCommands("RightPosRightSwitchAuto"))
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
        self.addSequential(LogCommands("RightPosLeftSwitchAuto"))
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
        self.addSequential(LogCommands("LeftPosRightSwitchAuto"))
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
        self.addSequential(LogCommands("LeftPosLeftSwitchAuto"))
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
        self.addSequential(LogCommands("LeftPosLeftScaleAuto"))
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
        self.addSequential(LogCommands("RightPosRightScaleAuto"))
        self.addSequential(Parallel(
            AutoEncoders(25.5),
        ))
        self.addSequential(AutoEncodersTurnLeft(90))
        self.addSequential(ElevatorScale())
        self.addSequential(SpitOut())
        self.addSequential(AutoEncoders(-3))
        self.addSequential(ElevatorSwitch())


class LeftPosRightScaleAuto(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__()
        self.addSequential(LogCommands("LeftPosRightScaleAuto"))
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
        self.addSequential(LogCommands("RightPosLeftScaleAuto"))
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

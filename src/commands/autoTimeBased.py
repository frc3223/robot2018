import wpilib
import wpilib.command
import wpilib.drive
import networktables
import commands
import commands.auto_conditions

class AutoTimeBased(wpilib.command.Command):
    def __init__(self):
        super().__init__("AutoTimeBased")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.Time_table = networktables.NetworkTables.getTable('/Time/')
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)

    def initialize(self):
        self.time = wpilib.Timer()
        self.time.start()

    def timereset(self):
        self.time.reset()

    def motorForward(self, power):
        self.drivetrain.motor_lb.set(power)
        self.drivetrain.motor_rb.set(-power)

    def motorturn(self, power):
        self.drivetrain.motor_rb.set(power)
        self.drivetrain.motor_lb.set(power)

    def execute(self):
        deltaTime = self.time.get()
        self.Time_table.putNumber("Time", deltaTime)
        if self.time.get() <=5.0:
            self.motorForward(0.2)
            voltage = 0.3
            self.elevator.ascend(voltage)

        if 5.0 <= self.time.get() <= 5.5:
            #should drive x feet then kills motor
            self.motorForward(0)


        elif 5.5 <= self.time.get() <= 6.5:
            # waits for half a sec then hopefully turns 90 degrees clockwise
            self.motorturn(0.4)

        elif self.time.get() >= 6.5:
            #stops again
            self.drivetrain.off()
            voltage = 0
            self.elevator.ascend(voltage)

    def isFinished(self):
        if self.time.get() <= 15:
            return False
        elif self.time.get() > 15:
            return True

    def end(self):
        self.drivetrain.off()
        self.time.stop()


class TimeBasedForward(wpilib.command.Command):
    def __init__(self,time):
        super().__init__("TimeBasedForward")
        self.time = time
        self.timer = wpilib.Timer()
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)

    def  initialize(self):
        self.timer.start()

    def motorset(self, power):
            self.drivetrain.motor_lb.set(power)
            self.drivetrain.motor_rb.set(-power)

    def execute(self):
        self.motorset(0.3)

    def isFinished(self):
        if self.timer.get() >= self.time:
            return True

    def end(self):
        self.drivetrain.off()
        self.timer.stop()


class TimeBasedTurn(wpilib.command.Command):
    def __init__(self, time):
        super().__init__("TimeBasedTurn")
        self.time = time
        self.timer = wpilib.Timer()
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)

    def initialize(self):
        self.timer.start()

    def motorset(self, power):
        self.drivetrain.motor_lb.set(power)
        self.drivetrain.motor_rb.set(power)

    def execute(self):
        self.motorset(0.4)

    def isFinished(self):
        if self.timer.get() >= self.time:
            return True

    def end(self):
        self.drivetrain.off()
        self.timer.stop()


class TimeBasedGrabber(wpilib.command.TimedCommand):
    def __init__(self, time):
        super().__init__("TimeBasedGrabber", time)
        self.intake = self.getRobot().intake
        self.requires(self.intake)

    def execute(self):
        self.intake.open2Grabber()

    def end(self):
        self.intake.grabberOff()


class TimeBasedElevator(wpilib.command.TimedCommand):
    def __init__(self, time):
        super().__init__("TimeBasedElevator", time)
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)

    def execute(self):
        self.elevator.ascend(0.4)

    def end(self):
        self.elevator.hover()


class TimeBasedStart(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("TimeBasedStart")
        self.addSequential(TimeBasedForward(5))
        self.addParallel(TimeBasedElevator(5))
        self.addSequential(TimeBasedTurn(1))
        self.addSequential(TimeBasedGrabber(1))


class TimeBasedCenter(wpilib.command.CommandGroup):
    def __init__(self):
        super().__init__("TimeBasedCenter")
        self.addSequential(TimeBasedForward(5))
        self.addParallel(TimeBasedElevator(5))
        self.addSequential(commands.auto_conditions.IfIsMiddlePosRightSwitch(TimeBasedGrabber(1)))

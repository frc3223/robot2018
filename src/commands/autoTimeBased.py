import wpilib
import wpilib.drive
import networktables
import commands

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

    def  initalize(self):
        self.timer.start()

    def motorset(self, power):
            self.drivetrain.motor_lb.set(power)
            self.drivetrain.motor_rb.set(-power)

    def execute(self):
        self.motorset(0.2)

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

    def initalize(self):
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


class TimeBasedGrabber(wpilib.command.Command):
    def __init__(self, time):
        super().__init__("TimeBasedGrabber")
        self.time = time
        self.timer = wpilib.Timer()
        self.intake = self.getRobot().intake
        self.requires(self.intake)

    def initalize(self):
        self.timer.start()

    def execute(self):
        self.intake.open2Grabber()

    def isFinished(self):
        if self.timer.get() >= self.time:
            return True

    def end(self):
        self.elevator.off()
        self.timer.stop()


class TimeBasedElevator(wpilib.command.Command):
    def __init__(self, time):
        super().__init__("TimeBasedElevator")
        self.time = time
        self.timer = wpilib.Timer()
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)

    def initalize(self):
        self.timer.start()

    def execute(self):
        self.elevator.ascend(0.3)

    def isFinished(self):
        if self.timer.get() >= self.time:
            return True

    def end(self):
        self.elevator.off()
        self.timer.stop()

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
        self.addSequential(IfIsRightSwitch(TimeBasedGrabber(1)))

class IfIsRightSwitch(wpilib.command.ConditionalCommand):
    def __init__(self,onTrue, onFalse = None):
        super().__init__("IfIsRightSwitch",onTrue,onFalse)

    def condition(self):
        gamecode = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if gamecode is None:
            return False
        if len(gamecode) != 3:
            return False
        if gamecode[0] == "r":
            return True
        return False






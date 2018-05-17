import wpilib
import wpilib.command
import wpilib.drive
import networktables
import commands
from oi import getJoystick


class AutoEncoders(wpilib.command.Command):
    def __init__(self, feet):
        super().__init__("AutoEncoders")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.encoderR = 0
        self.encoderL = 0
        self.feet = feet
        self.Rpower = 0
        self.Lpower = 0
        self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()

    def execute(self):
        self.encoderVal = self.feet * self.drivetrain.ratio - 1150 #Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
        self.encoderR = abs(self.drivetrain.getRightEncoder())
        self.encoderL = abs(self.drivetrain.getLeftEncoder())
        self.encoderDiff = self.encoderR - self.encoderL

        if self.encoderR < self.encoderVal:
            if self.encoderDiff >= 1000 and False:  # if left encoder is less than right
                self.Lpower = 0.6
            elif self.encoderDiff <= -1000 and False:  # if right is less than left
                self.Rpower = -0.6
            elif -1000 < self.encoderDiff < 1000:  # if they are relatively the same
                self.Rpower = -0.5
                self.Lpower = 0.5
            self.drivetrain.drive_forward(0.3)
            #self.drivetrain.motor_rb.set(self.Rpower)
            #self.drivetrain.motor_lb.set(self.Lpower)
        elif self.encoderL >= self.encoderVal:
            self.Rpower = 0
            self.Lpower = 0
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
            self.done = True


    def isFinished(self):
        if(self.done and self.drivetrain.motor_lb.getSelectedSensorVelocity(0) <= 30 and self.drivetrain.motor_rb.getSelectedSensorVelocity(0) <= 30):
            self.done = False
            return True
        else:
            return False

    def end(self):
        self.drivetrain.off()


class AutoEncodersTurnLeft(wpilib.command.Command):
    def __init__(self, degrees):
        super().__init__("AutoEncodersTurnLeft")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.encoderR = 0
        self.encoderL = 0
        self.degrees = degrees
        self.Rpower = 0
        self.Lpower = 0
        self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.voltage_ramp_off()

    def execute(self):
        self.encoderVal = self.degrees * 10 - 500 #Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
        self.encoderR = abs(self.drivetrain.getRightEncoder())
        self.encoderL = abs(self.drivetrain.getLeftEncoder())
        self.encoderDiff = self.encoderR - self.encoderL
        print("turn left", self.encoderR, self.encoderVal)

        if self.encoderR < self.encoderVal:
            self.Rpower = -0.7
            self.Lpower = -0.7
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
            self.drivetrain.drive.feed()
        elif self.encoderR >= self.encoderVal:
            self.Rpower = 0
            self.Lpower = 0
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
            self.done = True

    def isFinished(self):
        if(self.done and abs(self.drivetrain.motor_lb.getSelectedSensorVelocity(0)) <= 30 and abs(self.drivetrain.motor_rb.getSelectedSensorVelocity(0)) <= 30):
            self.done = False
            return True
        else:
            return False


class AutoEncodersTurnRight(wpilib.command.Command):
   def __init__(self, degrees):
       super().__init__("AutoEncodersTurnRight")
       self.requires(self.getRobot().drivetrain)
       self.drivetrain = self.getRobot().drivetrain
       self.encoderR = 0
       self.encoderL = 0
       self.degrees = degrees
       self.Rpower = 0
       self.Lpower = 0
       self.done = False

   def initialize(self):
        self.drivetrain.zeroEncoders()

   def execute(self):
       self.encoderVal = self.degrees * 10.5 - 310  # Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
       self.encoderR = abs(self.drivetrain.getRightEncoder())
       self.encoderL = abs(self.drivetrain.getLeftEncoder())
       self.encoderDiff = self.encoderR - self.encoderL

       if self.encoderR < self.encoderVal:
           self.Rpower = 0.5
           self.Lpower = 0.5
           self.drivetrain.motor_rb.set(self.Rpower)
           self.drivetrain.motor_lb.set(self.Lpower)
           self.drivetrain.drive.feed()
       elif self.encoderR >= self.encoderVal:
           self.Rpower = 0
           self.Lpower = 0
           self.drivetrain.motor_rb.set(self.Rpower)
           self.drivetrain.motor_lb.set(self.Lpower)
           self.done = True

   def isFinished(self):
       if (self.done and abs(self.drivetrain.motor_lb.getSelectedSensorVelocity(0)) <= 30 and abs(self.drivetrain.motor_rb.getSelectedSensorVelocity(0)) <= 30):
           self.done = False
           return True
       else:
           return False


class ElevatorPosition(wpilib.command.Command):
    def __init__(self, name, position):
        super().__init__(name)
        self.joystick = getJoystick()
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)
        self.position = position
        self.diff = 500

    def initialize(self):
        self.elevator.elevator_mode = "ElevatorPosition(%s)" % self.position

    def execute(self):
        if self.elevator.zeroed:
            if self.elevator.getEncoderPosition() < self.position - self.diff:
                self.elevator.test_drive_positive()
            elif self.elevator.getEncoderPosition() > self.position + self.diff:
                self.elevator.test_drive_negative()

    def isFinished(self):
        if self.joystick.getPOV(0) in (0,180):
            return True
        if not self.elevator.zeroed:
            return True
        return abs(self.elevator.getEncoderPosition() - self.position) < self.diff

    def end(self):
        self.elevator.elevator_mode = ""
        self.elevator.hover()

class ElevatorScale(ElevatorPosition):
    def __init__(self):
        super().__init__("ElevatorScale",30000)
        self.count = 0

    def isFinished(self):
        if self.elevator.getCurrent() >= 50:
            self.count += 1
        else:
            self.count = 0

        if self.count >= 10:
            return True
        return super().isFinished()

class ElevatorSwitch(ElevatorPosition):
    def __init__(self):
        super().__init__("ElevatorSwitch", 9000)


class ElevatorIntake(ElevatorPosition):
    def __init__(self):
        super().__init__("ElevatorIntake", 1500)

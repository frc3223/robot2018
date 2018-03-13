import wpilib
import wpilib.command
import wpilib.drive
import networktables
import commands


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
        self.encoderVal = self.feet * 880 - 2650 #Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
        self.encoderR = abs(self.drivetrain.getRightEncoder())
        self.encoderL = abs(self.drivetrain.getLeftEncoder())
        self.encoderDiff = self.encoderR - self.encoderL

        if self.encoderR < self.encoderVal:
            if self.encoderDiff >= 1000:  # if left encoder is less than right
                self.Lpower = 0.6
            elif self.encoderDiff <= -1000:  # if right is less than left
                self.Rpower = -0.6
            elif -1000 < self.encoderDiff < 1000:  # if they are relatively the same
                self.Rpower = -0.5
                self.Lpower = 0.5
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
        elif self.encoderR >= self.encoderVal:
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

    def execute(self):
        self.encoderVal = self.degrees * 14.5 - 710 #Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
        self.encoderR = abs(self.drivetrain.getRightEncoder())
        self.encoderL = abs(self.drivetrain.getLeftEncoder())
        self.encoderDiff = self.encoderR - self.encoderL

        if self.encoderR < self.encoderVal:
            self.Rpower = -0.4
            self.Lpower = -0.4
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
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
       self.encoderVal = self.degrees * 14.5 - 710  # Destination in feet converted to encoder ticks subracted by the error in encoder ticks to stop.
       self.encoderR = abs(self.drivetrain.getRightEncoder())
       self.encoderL = abs(self.drivetrain.getLeftEncoder())
       self.encoderDiff = self.encoderR - self.encoderL

       if self.encoderR < self.encoderVal:
           self.Rpower = 0.4
           self.Lpower = 0.4
           self.drivetrain.motor_rb.set(self.Rpower)
           self.drivetrain.motor_lb.set(self.Lpower)
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

import wpilib.command

from data_logger import DataLogger
from profiler import TrapezoidalProfile
from pidcontroller import PIDController
from drivecontroller import DriveController


class ProfiledForward(wpilib.command.Command):
    def __init__(self, distance_ft):
        super().__init__("ProfiledForward")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.dist_enc = distance_ft * self.drivetrain.ratio
        self.period = 0.01

        self.ctrl_heading = PIDController(
            Kp=0, Ki=0, Kd=0, Kf=0,
            source=self.drivetrain.getAngle,
            output=self.correct_heading,
            period=self.period,
        )
        self.ctrl_heading.setInputRange(-180, 180)
        self.ctrl_heading.setOutputRange(-0.5, 0.5)

        self.max_velocity = self.drivetrain.fps_to_encp100ms(3)
        self.max_acceleration = self.drivetrain.fps2_to_encpsp100ms(3)
        self.profiler_l = TrapezoidalProfile(
            cruise_v=self.max_velocity,
            a=self.max_acceleration,
            target_pos=self.dist_enc, 
            tolerance=(3/12.)*self.drivetrain.ratio, # 3 inches
        )
        self.profiler_r = TrapezoidalProfile(
            cruise_v=self.max_velocity,
            a=self.max_acceleration,
            target_pos=-self.dist_enc, 
            tolerance=(3/12.)*self.drivetrain.ratio, # 3 inches
        )
        self.ctrl_l = DriveController(
            Kp=0, Kd=0, 
            Ks=1.293985, Kv=0.014172, Ka=0.005938, 
            get_voltage=self.drivetrain.getVoltage,
            source=self.drivetrain.getLeftEncoderVelocity,
            output=self.drivetrain.setLeftMotor,
            period=self.period,
        )
        self.ctrl_l.setInputRange(-self.max_velocity, self.max_velocity)
        self.ctrl_r = DriveController(
            Kp=0, Kd=0, 
            Ks=1.320812, Kv=0.013736, Ka=0.005938, 
            get_voltage=self.drivetrain.getVoltage,
            source=self.drivetrain.getRightEncoderVelocity,
            output=self.drivetrain.setRightMotor,
            period=self.period,
        )
        self.ctrl_r.setInputRange(-self.max_velocity, self.max_velocity)

        self.target_v_l = 0
        self.target_v_r = 0
        self.target_a_l = 0
        self.target_a_r = 0
        self.pos_l = 0
        self.pos_r = 0

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.ctrl_l.enable()
        self.ctrl_r.enable()
        self.ctrl_heading.enable()
        self.logger = self.drivetrain.logger
        self.logger.add("profile_vel_r", lambda: self.target_v_r)
        self.logger.add("profile_vel_l", lambda: self.target_v_l)
        self.drivetrain.logger_enabled = True
        print ('pdf init')

    def execute(self):
        self.pos_l = self.drivetrain.getLeftEncoder()
        self.pos_r = self.drivetrain.getRightEncoder()

        self.profiler_l.calculate_new_velocity(self.pos_l, self.period)
        self.profiler_r.calculate_new_velocity(self.pos_r, self.period)

        self.ctrl_l.setSetpoint(self.profiler_l.current_target_v)
        self.ctrl_l.setAccelerationSetpoint(self.profiler_l.current_a)
        self.ctrl_r.setSetpoint(self.profiler_r.current_target_v)
        self.ctrl_r.setAccelerationSetpoint(self.profiler_r.current_a)

        self.drivetrain.feed()
        self.target_v_l = self.profiler_l.current_target_v
        self.target_v_r = self.profiler_r.current_target_v
        self.target_a_l = self.profiler_l.current_a
        self.target_a_r = self.profiler_r.current_a
        print ('pdf exec')

    def isFinished(self):
        return (
            abs(self.pos_l - self.dist_enc) < self.drivetrain.ratio * 1/.3 and
            self.profiler_l.current_target_v == 0 and
            self.profiler_l.current_a == 0 and 
            self.profiler_r.current_target_v == 0 and 
            self.profiler_r.current_a == 0)

    def end(self):
        self.ctrl_l.disable()
        self.ctrl_r.disable()
        self.ctrl_heading.disable()
        self.drivetrain.off()
        self.drivetrain.logger_enabled = False
        self.logger.flush()
        print ('pdf end')

    def correct_heading(self, correction):
        self.profiler_l.setCruiseVelocityScale(1+correction)
        self.profiler_r.setCruiseVelocityScale(1-correction)

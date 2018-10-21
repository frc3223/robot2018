import wpilib.command
from profiler import TrapezoidalProfile
from drivecontroller import DriveController


class ProfiledForward(wpilib.command.Command):
    def __init__(self, distance_ft):
        super().__init__("ProfiledForward")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.dist_enc = distance_ft * self.drivetrain.ratio

        self.profiler_l = TrapezoidalProfile(
            cruise_v=self.drivetrain.fps_to_encp100ms(8),
            a=self.drivetrain.fps2_to_encpsp100ms(4), 
            target_pos=self.dist_enc, 
            tolerance=(3/12.)*self.drivetrain.ratio, # 3 inches
        )
        self.profiler_r = TrapezoidalProfile(
            cruise_v=self.drivetrain.fps_to_encp100ms(8),
            a=self.drivetrain.fps2_to_encpsp100ms(4), 
            target_pos=-self.dist_enc, 
            tolerance=(3/12.)*self.drivetrain.ratio, # 3 inches
        )
        self.period = 0.02
        self.ctrl_l = DriveController(
            Kp=0, Kd=0, 
            Ks=1.293985, Kv=0.014172, Ka=0.005938, 
            get_voltage=self.drivetrain.getVoltage(),
            source=self.drivetrain.getLeftEncoderVelocity,
            output=self.drivetrain.setLeftMotor,
            period=self.period,
        )
        self.ctrl_r = DriveController(
            Kp=0, Kd=0, 
            Ks=1.320812, Kv=0.013736, Ka=0.005938, 
            get_voltage=self.drivetrain.getVoltage(),
            source=self.drivetrain.getRightEncoderVelocity,
            output=self.drivetrain.setRightMotor,
            period=self.period,
        )

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.ctrl_l.enable()
        self.ctrl_r.enable()

    def execute(self):
        pos_l = self.drivetrain.getLeftEncoder()
        pos_r = self.drivetrain.getRightEncoder()

        self.profiler_l.calculate_new_velocity(pos_l, self.period)
        self.profiler_r.calculate_new_velocity(pos_r, self.period)

        self.ctrl_l.setSetpoint(self.profiler_l.current_target_v)
        self.ctrl_l.setAccelerationSetpoint(self.profiler_l.current_a)
        self.ctrl_r.setSetpoint(self.profiler_r.current_target_v)
        self.ctrl_r.setAccelerationSetpoint(self.profiler_r.current_a)

    def isFinished(self):
        return (
            self.profiler_l.current_target_v == 0 and 
            self.profiler_l.current_a == 0 and 
            self.profiler_r.current_target_v == 0 and 
            self.profiler_r.current_a == 0)

    def end(self):
        self.ctrl_l.disable()
        self.ctrl_r.disable()
        self.drivetrain.off()

    

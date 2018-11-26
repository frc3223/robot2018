import csv
import math

from wpilib import Timer
from wpilib.command import Command

from commands.statespace import StateSpaceDriveController
from data_logger import DataLogger
from pidcontroller import PIDController
from drivecontroller import DriveController


def read_trajectories(fnom):
    from os.path import dirname, join
    trajectory_points = []
    with open(join(dirname(__file__), "..", "trajectories", fnom)) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                # header
                assert row == ['dt', 'xl', 'xr', 'vl', 'vr','al', 'ar', 'heading']
            else:
                trajectory_points.append(tuple(float(x) for x in row))

    return trajectory_points


class _CsvTrajectoryCommand(Command):
    def __init__(self, fnom, name=None):
        super().__init__(name)
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.timer = Timer()
        self.period = self.getRobot().getPeriod()
        self.fnom = fnom
        self.trajectory_points = read_trajectories(self.fnom)
        assert self.trajectory_points[0][0] == self.period
        self.i = 0

        self.target_v_l = 0
        self.target_v_r = 0
        self.target_a_l = 0
        self.target_a_r = 0
        self.target_heading = 0

    def get_trajectory_point_m(self, i):
        pt = (_, xl_m, xr_m, vl_mps, vr_mps, al_mps2, ar_mps2, heading_rad) = self.trajectory_points[i]
        return pt

    def get_trajectory_point_enc(self, i):
        (dt_s, xl_m, xr_m, vl_mps, vr_mps, al_mps2, ar_mps2, heading_rad) = self.trajectory_points[i]
        def m_to_enc(x):
            return self.drivetrain.ratio * x / 0.3048
        def mps_to_encp100ms(v):
            return self.drivetrain.fps_to_encp100ms(v / 0.3048)

        def mps2_to_encp100msps(a):
            return self.drivetrain.fps2_to_encpsp100ms(a / 0.3048)

        return (dt_s, m_to_enc(xl_m), m_to_enc(xr_m),
                mps_to_encp100ms(vl_mps), mps_to_encp100ms(vr_mps),
                mps2_to_encp100msps(al_mps2), mps2_to_encp100msps(ar_mps2),
                heading_rad)

    def isFinished(self):
        return self.i >= len(self.trajectory_points)


class CsvTrajectoryCommand(_CsvTrajectoryCommand):
    def __init__(self, fnom):
        super().__init__(fnom)
        self.ctrl_heading = PIDController(
            Kp=0, Ki=0, Kd=0, Kf=0,
            source=self.drivetrain.getAngle,
            output=self.correct_heading,
            period=self.period,
        )
        self.ctrl_heading.setInputRange(-180, 180)
        self.ctrl_heading.setOutputRange(-0.5, 0.5)
        self.ctrl_heading.setContinuous(True)

        self.max_velocity_fps = 11
        self.max_velocity_encps = self.drivetrain.fps_to_encp100ms(self.max_velocity_fps)
        self.ctrl_l = DriveController(
            Kp=0, Kd=0,
            Ks=1.293985, Kv=0.014172, Ka=0.005938,
            get_voltage=self.drivetrain.getVoltage,
            source=self.drivetrain.getLeftEncoderVelocity,
            output=self.drivetrain.setLeftMotor,
            period=self.period,
        )
        self.ctrl_l.setInputRange(-self.max_velocity_encps, self.max_velocity_encps)
        self.ctrl_r = DriveController(
            Kp=0, Kd=0,
            Ks=1.320812, Kv=0.013736, Ka=0.005938,
            get_voltage=self.drivetrain.getVoltage,
            source=self.drivetrain.getRightEncoderVelocity,
            output=self.drivetrain.setRightMotor,
            period=self.period,
        )
        self.ctrl_r.setInputRange(-self.max_velocity_encps, self.max_velocity_encps)

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.ctrl_l.enable()
        self.ctrl_r.enable()
        self.ctrl_heading.enable()
        self.logger = DataLogger("csv_trajectory1.csv")
        self.drivetrain.init_logger(self.logger)
        self.logger.add("profile_vel_r", lambda: self.target_v_r)
        self.logger.add("profile_vel_l", lambda: self.target_v_l)
        self.logger.add("pos_ft_l", lambda: self.pos_ft_l)
        self.logger.add("i", lambda: self.i)
        self.timer.start()
        self.i = 0
        #print ('pdf init')

    def execute(self):
        self.pos_ft_l = self.drivetrain.getLeftEncoder() / self.drivetrain.ratio
        self.pos_ft_r = self.drivetrain.getRightEncoder() / self.drivetrain.ratio

        (_, _, _, self.target_v_l, self.target_v_r, self.target_a_l,
         self.target_a_r, self.target_heading) = self.get_trajectory_point_enc(self.i)

        self.ctrl_l.setSetpoint(self.target_v_l)
        self.ctrl_l.setAccelerationSetpoint(self.target_a_l)
        self.ctrl_r.setSetpoint(self.target_v_r)
        self.ctrl_r.setAccelerationSetpoint(self.target_a_r)
        self.ctrl_heading.setSetpoint(self.target_heading)

        self.drivetrain.feed()
        self.logger.log()
        self.i += 1

    def end(self):
        self.ctrl_l.disable()
        self.ctrl_r.disable()
        self.ctrl_heading.disable()
        self.drivetrain.off()
        self.logger.flush()
        #print ('pdf end')

    def correct_heading(self, correction):
        pass


class StateSpaceDriveCommand(_CsvTrajectoryCommand, StateSpaceDriveController):
    def __init__(self, fnom):
        _CsvTrajectoryCommand.__init__(self, fnom)
        StateSpaceDriveController.__init__(self, Command.getRobot().drivetrain)
        self.u_min = -8
        self.u_max = 8

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.i = 0
        self.logger = DataLogger("ss_trajectory.csv")
        self.drivetrain.init_logger(self.logger)

    def execute(self):
        (dt_s, xl_m, xr_m, vl_mps, vr_mps, al_mps2, ar_mps2, heading_rad) = self.get_trajectory_point_m(self.i)
        self.update(xl_m, xr_m, vl_mps, vr_mps)
        self.logger.log()
        self.i += 1

    def end(self):
        self.drivetrain.off()
        self.logger.flush()

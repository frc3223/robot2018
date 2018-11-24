import pytest
from unittest.mock import MagicMock
from data_logger import DataLogger
from commands.trajectories import CsvTrajectoryCommand, StateSpaceDriveCommand
from robot import Rockslide


log_trajectory = True


def test_CsvTrajectoryCommand(Notifier):
    robot = Rockslide()
    robot.robotInit()
    command = CsvTrajectoryCommand("traj1.tra")
    command.initialize()
    i = 0
    t = 0
    while not command.isFinished():
        command.execute()
        i += 1
        t += robot.getPeriod()

        assert t < 10

    command.end()

class DriveSide:
    def __init__(self, Ks, Kv, Ka, invert=False):
        s = self
        s.Ks, s.Kv, s.Ka, s.invert = Ks, Kv, Ka, invert
        print("Ks: %f" % Ks)
        print("Kv: %f" % Kv)
        print("Ka: %f" % Ka)
        self.v_mps = 0
        self.a_mps2 = 0
        self.pos_m = 0

    def update(self, voltage, dt_s):
        if self.invert:
            voltage = -voltage
        Ks = self.Ks
        if voltage < 0: Ks = -Ks
        self.pos_m += self.v_mps * dt_s
        self.v_mps += self.a_mps2 * dt_s
        self.a_mps2 = (voltage - Ks - self.v_mps * self.Kv) / self.Ka


def test_DriveSide():
    ds = DriveSide(Ks=1, Kv=2, Ka=3)
    ds.update(10, 0.02)
    assert ds.a_mps2 == pytest.approx(3.0, 0.01)
    assert ds.v_mps == pytest.approx(0.0, 0.01)
    ds.update(10, 0.02)
    assert ds.a_mps2 == pytest.approx(2.96, 0.01)
    assert ds.v_mps == pytest.approx(0.06, 0.01)
    ds.update(-10, 0.02)
    assert ds.a_mps2 == pytest.approx(-3.08, 0.01)
    assert ds.v_mps == pytest.approx(0.1192, 0.01)
    ds.update(-10, 0.02)
    assert ds.a_mps2 == pytest.approx(-3.04, 0.01)
    assert ds.v_mps == pytest.approx(0.0576, 0.01)
    ds.update(-10, 0.02)
    assert ds.a_mps2 == pytest.approx(-2.99, 0.01)
    assert ds.v_mps == pytest.approx(-0.00315, 0.01)


def test_DriveSide2():
    ds = DriveSide(Ks=1, Kv=2, Ka=3, invert=True)
    ds.update(10, 0.02)
    assert ds.pos_m == pytest.approx(0, 0.01)
    ds.update(10, 0.02)
    assert ds.pos_m == pytest.approx(0, 0.01)
    ds.update(10, 0.02)
    assert ds.pos_m == pytest.approx(-0.0012, 0.01)
    ds.update(10, 0.02)
    assert ds.pos_m == pytest.approx(-0.00358, 0.01)


def test_StateSpaceDriveCommand(Notifier):
    global log_trajectory
    left_drive = DriveSide(
            Ks=1.293985, 
            Kv=0.014172 * 63. / 0.3048, 
            Ka=0.005938 * 63. / 0.3048)
    right_drive = DriveSide(
            Ks=1.320812, 
            Kv=0.013736 * 63. / 0.3048, 
            Ka=0.005938 * 63. / 0.3048)

    robot = Rockslide()
    robot.robotInit()
    robot.drivetrain.getLeftEncoder = getLeftEncoder = MagicMock()
    robot.drivetrain.getRightEncoder = getRightEncoder = MagicMock()
    robot.drivetrain.getVoltage = MagicMock(return_value=10)
    command = StateSpaceDriveCommand("straight3m.tra")
    command.initialize()
    dt = robot.getPeriod()
    t = 0

    if log_trajectory:
        logger = DataLogger("test_StateSpaceDriveCommand.csv")
        logger.log_while_disabled = True
        logger.do_print = False
        logger.add('t', lambda: t)
        logger.add('pos_l_m', lambda: left_drive.pos_m)
        logger.add('pos_r_m', lambda: right_drive.pos_m)
        logger.add('m_pos_l_m', lambda: command.y[0,0])
        logger.add('m_pos_r_m', lambda: command.y[1,0])
        logger.add('vel_l_mps', lambda: left_drive.v_mps)
        logger.add('vel_r_mps', lambda: right_drive.v_mps)
        logger.add('target_pos_l_m', lambda: command.r[0,0])
        logger.add('target_pos_r_m', lambda: command.r[2,0])
        logger.add('target_vel_l_mps', lambda: command.r[1,0])
        logger.add('target_vel_r_mps', lambda: command.r[3,0])
        logger.add('voltage', lambda: command.drivetrain.getVoltage())
        logger.add('vpl', lambda: command.drivetrain.motor_lb.get())
        logger.add('vpr', lambda: command.drivetrain.motor_lb.get())

    while not command.isFinished():
        logger.log()
        getLeftEncoder.return_value = left_drive.pos_m * 630 / 0.3048
        getRightEncoder.return_value = right_drive.pos_m * 630 / 0.3048
        command.execute()

        V = command.drivetrain.getVoltage()
        vpl = command.drivetrain.motor_lb.get()
        vpr = command.drivetrain.motor_rb.get()
        left_drive.update(V * vpl, dt)
        right_drive.update(V * vpr, dt)
        t += dt

        assert t < 10

    command.end()

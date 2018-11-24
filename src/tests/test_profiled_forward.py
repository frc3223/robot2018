from unittest.mock import MagicMock
from data_logger import DataLogger

from robot import Rockslide
from commands.profiled_forward import ProfiledForward


def test_ProfiledForward1(Notifier):
    robot = Rockslide()
    robot.robotInit()

    command = ProfiledForward(10)
    command.initialize()
    command.execute()
    command.isFinished()
    command.end()


log_trajectory = True


def test_ProfiledForward2(Notifier, sim_hooks):
    global log_trajectory
    robot = Rockslide()
    robot.robotInit()
    DT = robot.getPeriod()

    robot.drivetrain.getLeftEncoder = getLeftEncoder = MagicMock()
    robot.drivetrain.getRightEncoder = getRightEncoder = MagicMock()
    getLeftEncoder.return_value = 0
    getRightEncoder.return_value = 0
    command = ProfiledForward(10)
    command.initialize()

    t = 0
    pos_ft = 0

    if log_trajectory:
        logger = DataLogger("test_profiled_forward2.csv")
        logger.log_while_disabled = True
        logger.do_print = True
        logger.add('t', lambda: t)
        logger.add('pos', lambda: pos_ft)
        logger.add('target_pos', lambda: command.dist_ft)
        logger.add('v', lambda: command.profiler_l.current_target_v)
        logger.add('max_v', lambda: command.max_v_encps)
        logger.add('a', lambda: command.profiler_l.current_a)
        logger.add('max_a', lambda: command.max_acceleration)
        logger.add('voltage', lambda: command.drivetrain.getVoltage())
        logger.add('vpl', lambda: command.drivetrain.motor_lb.get())
        logger.add('adist', lambda: command.profiler_l.adist)
        logger.add('err', lambda: command.profiler_l.err)
    while t < 10:
        if log_trajectory:
            logger.log()
        getLeftEncoder.return_value = pos_ft * command.drivetrain.ratio
        getRightEncoder.return_value = -pos_ft * command.drivetrain.ratio

        command.execute()

        v = command.profiler_l.current_target_v
        pos_ft += v * DT
        t += DT
        sim_hooks.time = t

        if command.isFinished():
            break

    command.end()
    if log_trajectory:
        logger.log()
        logger.close()

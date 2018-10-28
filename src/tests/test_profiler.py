import pytest

from data_logger import DataLogger
from profiler import TrapezoidalProfile


def test_cruise_velocity_positive1():
    """
    cruise velocity must always be positive
    """
    with pytest.raises(AssertionError):
        profiler = TrapezoidalProfile(cruise_v=-10, a=20, target_pos=0, tolerance=.5)


def test_cruise_velocity_positive2():
    """
    cruise velocity must always be positive
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=0, tolerance=.5)
    with pytest.raises(AssertionError):
        profiler.setCruiseVelocityScale(-1)


def test_cruise_velocity_positive3():
    """
    cruise velocity must always be positive
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=0, tolerance=.5)

    # i will hurt anyone who actually does this
    profiler._cruise_v = -10
    with pytest.raises(AssertionError):
        profiler.calculate_new_velocity(0, 0.01)


def test_target_position_may_be_negative():
    """
    target position may be negative
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=-1000, tolerance=.5)



def test_target_velocity_may_be_negative():
    """
    target position may be negative
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=-1000, tolerance=.5)

    profiler.calculate_new_velocity(0, 0.01)
    assert profiler.current_target_v < 0
    assert profiler.current_a < 0


@pytest.mark.parametrize("target_pos, current_pos, expectedResult", [
    (0, 0, True),
    (0, 0.51, False),
    (0, 0.5, False),
    (0, 0.499, True),
    (0, -0.499, True),
    (0, -0.5, False),
    (0, -0.51, False),
])
def test_isFinished1(target_pos, current_pos, expectedResult):
    """
    when not moving, velocity=0, we are done when our current position is within tolerance of the target position
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=target_pos, tolerance=.5, current_target_v=0)

    assert profiler.isFinished(current_pos) == expectedResult


def test_isFinished2():
    """
    when moving, we are not done even when our current position is within tolerance of the target position because
    overshoot has happened
    """
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=0, tolerance=.5, current_target_v=10)

    assert profiler.isFinished(0) == False


log_trajectory = False

def test_profiler1():
    """
    forward velocity, trapezoid, no overshoot
    """

    DT = 0.02
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=50, tolerance=.5, current_target_v=0)

    t = 0
    pos = 0

    if log_trajectory:
        logger = DataLogger("test_profiler1.csv")
        logger.log_while_disabled = True
        logger.do_print = True
        logger.add('t', lambda: t)
        logger.add('pos', lambda: pos)
        logger.add('v', lambda: profiler.current_target_v)
        logger.add('a', lambda: profiler.current_a)

    while not profiler.isFinished(pos):
        if log_trajectory:
            logger.log()
        profiler.calculate_new_velocity(pos, DT)

        pos += profiler.current_target_v * DT
        t += DT

        if t > 10:
            if log_trajectory:
                logger.close()
            assert False, "sim loop timed out"

        if t < 0.501:
            assert profiler.current_a == pytest.approx(20, 0.01), "t = %f" % (t,)
        if 0.501 < t < 5:
            assert profiler.current_target_v == pytest.approx(10., 0.01), "t = %f" % (t,)
            assert profiler.current_a == 0, "t = %f" % (t,)
        if 5 < t < 5.5 - 0.001:
            assert profiler.current_a == pytest.approx(-20., 0.01), "t = %f" % (t,)
        if t == pytest.approx(5.50, 0.001):
            assert profiler.current_a == pytest.approx(0., 0.01), "t = %f" % (t,)
            assert profiler.current_target_v == pytest.approx(0., 0.01), "t = %f" % (t,)

    if log_trajectory:
        logger.log()
        logger.close()

    assert t == pytest.approx(5.52, 0.01)
    assert profiler.current_a == 0


def test_profiler2():
    """
    forward velocity, triangle, no overshoot
    """

    DT = 0.02
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=4, tolerance=.5, current_target_v=0)

    t = 0
    pos = 0

    if log_trajectory:
        logger = DataLogger("test_profiler2.csv")
        logger.log_while_disabled = True
        logger.add('t', lambda: t)
        logger.add('pos', lambda: pos)
        logger.add('v', lambda: profiler.current_target_v)
        logger.add('a', lambda: profiler.current_a)

    while not profiler.isFinished(pos):
        if log_trajectory:
            logger.log()
        profiler.calculate_new_velocity(pos, DT)

        pos += profiler.current_target_v * DT
        t += DT

        if t > 10:
            if log_trajectory:
                logger.close()
            assert False, "sim loop timed out"

        if t < 0.4599:
            assert profiler.current_a == pytest.approx(20, 0.01), "t = %f" % (t,)

        if t == pytest.approx(0.46, 0.01):
            assert profiler.current_target_v == pytest.approx(9.2, 0.01)
            assert profiler.current_a == pytest.approx(20, 0.01), "t = %f" % (t,)
        if 0.4601 < t < 0.92:
            assert profiler.current_a == pytest.approx(-20, 0.01), "t = %f" % (t,)

    if log_trajectory:
        logger.log()
        logger.close()

    assert 0.8 < t < 1.0
    assert profiler.current_a == 0


def test_profiler3():
    """
    reverse velocity, trapezoid, no overshoot
    """

    DT = 0.02
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=-50, tolerance=.5, current_target_v=0)

    t = 0
    pos = 0

    if log_trajectory:
        logger = DataLogger("test_profiler3.csv")
        logger.log_while_disabled = True
        logger.add('t', lambda: t)
        logger.add('pos', lambda: pos)
        logger.add('v', lambda: profiler.current_target_v)
        logger.add('a', lambda: profiler.current_a)

    while not profiler.isFinished(pos):
        if log_trajectory:
            logger.log()
        profiler.calculate_new_velocity(pos, DT)

        pos += profiler.current_target_v * DT
        t += DT

        if t > 10:
            if log_trajectory:
                logger.close()
            assert False, "sim loop timed out"

        if t < 0.501:
            assert profiler.current_a == pytest.approx(-20, 0.01), "t = %f" % (t,)
        if 0.501 < t < 5.0-0.001:
            assert profiler.current_target_v == pytest.approx(-10., 0.01), "t = %f" % (t,)
            assert profiler.current_a == 0, "t = %f" % (t,)
        if 5.0 < t < 5.52-0.001:
            assert profiler.current_a == pytest.approx(20, 0.01), "t = %f" % (t,)


    if log_trajectory:
        logger.log()
        logger.close()

    assert 5 < t < 6
    assert profiler.current_a == 0


def test_profiler4():
    """
    reverse velocity, triangle, no overshoot
    """

    DT = 0.02
    profiler = TrapezoidalProfile(cruise_v=10, a=20, target_pos=-4, tolerance=.5, current_target_v=0)

    t = 0
    pos = 0

    if log_trajectory:
        logger = DataLogger("test_profiler4.csv")
        logger.log_while_disabled = True
        logger.add('t', lambda: t)
        logger.add('pos', lambda: pos)
        logger.add('v', lambda: profiler.current_target_v)
        logger.add('a', lambda: profiler.current_a)

    while not profiler.isFinished(pos):
        if log_trajectory:
            logger.log()
        profiler.calculate_new_velocity(pos, DT)

        pos += profiler.current_target_v * DT
        t += DT

        if t > 10:
            if log_trajectory:
                logger.close()
            assert False, "sim loop timed out"

        if t < 0.4599:
            assert profiler.current_a == pytest.approx(-20, 0.01), "t = %f" % (t,)

        if t == pytest.approx(0.46, 0.01):
            assert profiler.current_target_v == pytest.approx(-9.2, 0.01)
            assert profiler.current_a == pytest.approx(-20, 0.01), "t = %f" % (t,)
        if 0.4601 < t < 0.92:
            assert profiler.current_a == pytest.approx(20, 0.01), "t = %f" % (t,)

    if log_trajectory:
        logger.log()
        logger.close()

    assert t == pytest.approx(0.94, 0.01)
    assert profiler.current_a == 0

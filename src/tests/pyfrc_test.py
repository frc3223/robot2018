'''
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
'''
from pyfrc.tests import *
import pytest
import math
from profiler import TrapezoidalProfile

def test_profiler():
    # 3 m/s, 4 m/s^2, 18 m, 0.5 m
    profiler = TrapezoidalProfile(cruise_v=3, a=4, target_pos=18, tolerance=0.5)

    assert math.isclose(profiler.current_target_v, 0)

    profiler.calculate_new_velocity(0, 0.02)

    assert math.isclose(profiler.current_target_v, 0.08)

    profiler.calculate_new_velocity(0.1, 0.02)

    assert math.isclose(profiler.current_target_v, 0.16)

    profiler.calculate_new_velocity(17.99, 0.02)
    assert math.isclose(profiler.current_target_v, 0.08)
    profiler.calculate_new_velocity(18.00, 0.02)
    assert math.isclose(profiler.current_target_v, 0.00)


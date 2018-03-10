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

def test_waitforautoinput():
    import networktables 
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putBoolean("switchAttempt", True)
    from commands.autoIn import WaitForAutoIn

    command = WaitForAutoIn()

    result = command.isFinished()

    assert result == False

    table.putBoolean("scaleAttempt", True)

    result = command.isFinished()

    assert result == False

    table.putString("autonomousMode", "tacos")

    result = command.isFinished()

    assert result == True

@pytest.mark.parametrize("nt_value, expected", [
    ("tacos", False),
    ("Middle", True),
    (None, False),
])
def test_IfIsMiddlePos(nt_value, expected):
    from commands.autoIn import IfIsMiddlePos
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", nt_value)
    command = IfIsMiddlePos(None, None)

    result = command.condition()

    assert result == expected

@pytest.mark.parametrize("nt_value, expected", [
    ("tacos", False),
    ("Left", True),
    (None, False),
])
def test_IfIsLeftPos(nt_value, expected):
    from commands.autoIn import IfIsLeftPos
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", nt_value)
    command = IfIsLeftPos(None, None)

    result = command.condition()

    assert result == expected

@pytest.mark.parametrize("nt_value, expected", [
    ("tacos", False),
    ("Right", True),
    (None, False),
])
def test_IfIsRightPos(nt_value, expected):
    from commands.autoIn import IfIsRightPos
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", nt_value)
    command = IfIsRightPos(None, None)

    result = command.condition()

    assert result == expected

@pytest.mark.parametrize("nt_value, expected", [
    (False, False),
    (True, True),
    (None, False),
])
def test_IfIsSwitch(nt_value, expected):
    from commands.autoIn import IfSwitch
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putBoolean("switchAttempt", nt_value)
    command = IfSwitch(None, None)

    result = command.condition()

    assert result == expected

@pytest.mark.parametrize("nt_value, expected", [
    (False, False),
    (True, True),
    (None, False),
])
def test_IfIsScale(nt_value, expected):
    from commands.autoIn import IfScale
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putBoolean("scaleAttempt", nt_value)
    command = IfScale(None, None)

    result = command.condition()

    assert result == expected
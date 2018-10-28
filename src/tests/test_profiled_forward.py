from unittest.mock import MagicMock

import pytest

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

def test_ProfiledForward2(Notifier):
    robot = Rockslide()
    robot.robotInit()

    robot.drivetrain.getLeftEncoder = getLeftEncoder = MagicMock()
    robot.drivetrain.getRightEncoder = getRightEncoder = MagicMock()
    getLeftEncoder.return_value = 21
    getRightEncoder.return_value = -7
    command = ProfiledForward(10)
    command.initialize()

    assert command.isFinished() == False
    command.execute()

    assert command.target_v_l == pytest.approx(1.89, 0.01)
    assert command.target_v_r == pytest.approx(-1.89, 0.01)

    getLeftEncoder.return_value = 66
    getRightEncoder.return_value = -30
    command.execute()

    assert command.target_v_l == pytest.approx(3.78, 0.01)
    assert command.target_v_r == pytest.approx(-3.78, 0.01)
    assert command.isFinished() == False

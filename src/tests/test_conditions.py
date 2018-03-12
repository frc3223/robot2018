import pytest
from unittest.mock import patch


@pytest.mark.parametrize("nt_value, expected", [
    ("tacos", False),
    ("Middle", True),
    (None, False),
])
def test_IfIsMiddlePos(nt_value, expected):
    from commands.auto_conditions import IfIsMiddlePos
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
    from commands.auto_conditions import IfIsLeftPos
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
    from commands.auto_conditions import IfIsRightPos
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
    from commands.auto_conditions import IfSwitch
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
    from commands.auto_conditions import IfScale
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putBoolean("scaleAttempt", nt_value)
    command = IfScale(None, None)

    result = command.condition()

    assert result == expected


@pytest.mark.parametrize("autoMode, switchAttempt, gamecode, expected", [
    (None, False, None, False),
    ("", True, "", False),
    ("Right", True, "", False),
    ("Left", True, "rlr", False),
    ("Right", True, "lrl", False),
    ("Right", False, "rrr", False),
    ("Right", True, "rrr", True),
    ("Right", True, "rlr", True),
    ("Right", True, "RRR", True),
    ("Right", True, "RLR", True),
])
def test_IfIsRightPosRightSwitch(autoMode, switchAttempt, gamecode, expected):
    from commands.auto_conditions import IfIsRightPosRightSwitch as TestCommand
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", autoMode)
    table.putBoolean("switchAttempt", switchAttempt)
    with patch('wpilib.DriverStation.getGameSpecificMessage') as getGameSpecificMessage:
        getGameSpecificMessage.return_value = gamecode

        command = TestCommand(None, None)

        result = command.condition()

        assert result == expected


@pytest.mark.parametrize("autoMode, switchAttempt, gamecode, expected", [
    (None, False, None, False),
    ("", True, "", False),
    ("Left", True, "", False),
    ("Right", True, "lrl", False),
    ("Left", True, "rlr", False),
    ("Left", False, "lrl", False),
    ("Left", True, "lrl", True),
    ("Left", True, "lll", True),
    ("Left", True, "LRL", True),
    ("Left", True, "LLL", True),
])
def test_IfIsLeftPosLeftSwitch(autoMode, switchAttempt, gamecode, expected):
    from commands.auto_conditions import IfIsLeftPosLeftSwitch as TestCommand
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", autoMode)
    table.putBoolean("switchAttempt", switchAttempt)
    with patch('wpilib.DriverStation.getGameSpecificMessage') as getGameSpecificMessage:
        getGameSpecificMessage.return_value = gamecode

        command = TestCommand(None, None)

        result = command.condition()

        assert result == expected


@pytest.mark.parametrize("autoMode, switchAttempt, gamecode, expected", [
    (None, False, None, False),
    ("", True, "", False),
    ("Middle", True, "", False),
    ("Right", True, "rlr", False),
    ("Middle", True, "lrl", False),
    ("Middle", False, "rlr", False),
    ("Middle", True, "rlr", True),
    ("Middle", True, "rrr", True),
    ("Middle", True, "RLR", True),
    ("Middle", True, "RRR", True),
])
def test_IfIsMiddlePosRightSwitch(autoMode, switchAttempt, gamecode, expected):
    from commands.auto_conditions import IfIsMiddlePosRightSwitch as TestCommand
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putString("autonomousMode", autoMode)
    table.putBoolean("switchAttempt", switchAttempt)
    with patch('wpilib.DriverStation.getGameSpecificMessage') as getGameSpecificMessage:
        getGameSpecificMessage.return_value = gamecode

        command = TestCommand(None, None)

        result = command.condition()

        assert result == expected


def test_WaitForAutoIn():
    import networktables
    table = networktables.NetworkTables.getTable("SmartDashboard")
    table.putBoolean("switchAttempt", True)
    from commands.auto_conditions import WaitForAutoIn

    command = WaitForAutoIn()

    result = command.isFinished()

    assert result == False

    table.putBoolean("scaleAttempt", True)

    result = command.isFinished()

    assert result == False

    table.putString("autonomousMode", "tacos")

    result = command.isFinished()

    assert result == True



def test_WaitForGamecode():
    from commands.auto_conditions import WaitForGamecode
    with patch('wpilib.DriverStation.getGameSpecificMessage') as getGameSpecificMessage:
        command = WaitForGamecode()
        getGameSpecificMessage.return_value = None

        assert command.isFinished() == False
        getGameSpecificMessage.return_value = ""
        assert command.isFinished() == False
        getGameSpecificMessage.return_value = 1
        assert command.isFinished() == False
        getGameSpecificMessage.return_value = "lrl"
        assert command.isFinished() == True

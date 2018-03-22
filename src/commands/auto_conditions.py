import wpilib.command
import networktables


def is_middle_position():
    table = networktables.NetworkTables.getTable("SmartDashboard")
    return table.getString("autonomousMode", None) == "Middle"


def is_left_position():
    table = networktables.NetworkTables.getTable("SmartDashboard")
    return table.getString("autonomousMode", None) == "Left"


def is_right_position():
    table = networktables.NetworkTables.getTable("SmartDashboard")
    return table.getString("autonomousMode", None) == "Right"


def get_gamecode():
    gamecode = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if gamecode is None or not isinstance(gamecode, str):
        gamecode = ""
    return gamecode.lower()


def is_right_switch():
    return get_gamecode()[:1] == "r"


def is_left_switch():
    return get_gamecode()[:1] == "l"


def should_attempt_switch():
    table = networktables.NetworkTables.getTable("SmartDashboard")
    return table.getBoolean("switchAttempt", False)


def should_attempt_scale():
    table = networktables.NetworkTables.getTable("SmartDashboard")
    return table.getBoolean("scaleAttempt", False)


class IfIsMiddlePos(wpilib.command.ConditionalCommand):
    def condition(self): return is_middle_position()


class IfIsLeftPos(wpilib.command.ConditionalCommand):
    def condition(self): return is_left_position()


class IfIsRightPos(wpilib.command.ConditionalCommand):
    def condition(self): return is_right_position()


class IfSwitch(wpilib.command.ConditionalCommand):
    def condition(self): return should_attempt_switch()


class IfScale(wpilib.command.ConditionalCommand):
    def condition(self): return should_attempt_scale()


class IfIsRightPosRightSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfIsRightPosRightSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_right_position() and is_right_switch()


class IfIsRightPosLeftSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfisRIghtposLeftSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_right_position() and is_left_switch()


class IfIsMiddlePosRightSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfIsMiddlePosRightSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_middle_position() and is_right_switch()



class IfIsMiddlePosLeftSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfIsMiddlePosLeftSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_middle_position() and is_left_switch()


class IfIsLeftPosRightSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfIsLeftPosRightSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_left_position() and is_right_switch()


class IfIsLeftPosLeftSwitch(wpilib.command.ConditionalCommand):
    def __init__(self, onTrue, onFalse):
        super().__init__('IfIsLeftPosLeftSwitch', onTrue, onFalse)

    def condition(self):
        return should_attempt_switch() and is_left_position() and is_left_switch()


class WaitForAutoIn(wpilib.command.Command):
    def __init__(self):
        super().__init__("WaitForAutoIn", 5)

    def isFinished(self):
        if self.isTimedOut():
            return True
        table = networktables.NetworkTables.getTable("SmartDashboard")
        check_scale = table.getBoolean("scaleAttempt", None)
        check_switch = table.getBoolean("switchAttempt", None)
        check_lane = table.getString("autonomousMode", None)
        if check_scale is None or check_switch is None or check_lane is None:
            return False
        return True


class WaitForGamecode(wpilib.command.Command):
    def __init__(self):
        super().__init__("WaitForGamecode", 5)

    def isFinished(self):
        return len(get_gamecode()) == 3 or self.isTimedOut()


class Parallel(wpilib.command.CommandGroup):
    def __init__(self, *commands):
        super().__init__()
        for command in commands:
            self.addParallel(command)


class Sequential(wpilib.command.CommandGroup):
    def __init__(self, *commands):
        super().__init__()
        for command in commands:
            self.addSequential(command)
import wpilib
import networktables

class IfIsMiddlePos(wpilib.command.ConditionalCommand):

    def condition(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        return table.getString("autonomousMode", None) == "Middle"

class IfIsLeftPos(wpilib.command.ConditionalCommand):

    def condition(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        return table.getString("autonomousMode", None) == "Left"

class IfIsRightPos(wpilib.command.ConditionalCommand):

    def condition(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        return table.getString("autonomousMode", None) == "Right"

class IfSwitch(wpilib.command.ConditionalCommand):

    def condition(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        return table.getBoolean("switchAttempt", None)

class IfScale(wpilib.command.ConditionalCommand):

    def condition(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        return table.getBoolean("scaleAttempt", None)

class WaitForAutoIn(wpilib.command.Command):

    def isFinished(self):
        table = networktables.NetworkTables.getTable("SmartDashboard")
        checkScale = table.getBoolean("scaleAttempt",None)
        checkSwitch = table.getBoolean("switchAttempt",None)
        checkLane = table.getString("autonomousMode", None)
        if checkScale is None or checkSwitch is None or checkLane is None:
            return False
        return True
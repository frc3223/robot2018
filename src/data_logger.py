import csv
import os.path
from collections import OrderedDict
import time

import wpilib

class DataLogger:
    def __init__(self, fnom):
        self.data_getters = OrderedDict()
        filepath = os.path.join('/home/lvuser/', fnom)
        if wpilib.RobotBase.isSimulation():
            filepath = os.path.join('.', str(int(time.time())) + fnom)
        self.writer = csv.writer(open(filepath, 'w'))
        self.header_logged = False

    def add(self, name, getter):
        self.data_getters[name] = getter

    def log(self):
        if wpilib.DriverStation.getInstance().isDisabled():
            return
        if not self.header_logged:
            self.log_header()
        row = []
        for key in self.data_getters.keys():
            row.append(self.data_getters[key]())
        self.writer.writerow(row)

    def log_header(self):
        self.writer.writerow(self.data_getters.keys())
        self.header_logged = True


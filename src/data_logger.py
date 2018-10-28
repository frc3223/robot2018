import csv
import os.path
from collections import OrderedDict
import time

import wpilib

class DataLogger:
    def __init__(self, fnom, time_in_name=False):
        self.data_getters = OrderedDict()
        if time_in_name:
            fnom = fnom + '-' + str(int(time.time()))
        filepath = os.path.join('/home/lvuser/', fnom)
        if wpilib.RobotBase.isSimulation():
            filepath = os.path.join('../../logs', fnom)
        self.file = open(filepath, 'w')
        self.writer = csv.writer(self.file)
        self.header_logged = False
        self.log_while_disabled = False

    def add(self, name, getter):
        self.data_getters[name] = getter

    def log(self):
        if wpilib.DriverStation.getInstance().isDisabled() and not self.log_while_disabled:
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

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

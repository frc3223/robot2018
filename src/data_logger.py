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
        self.timer = wpilib.Timer()
        self.timer.start()

    def add(self, name, getter):
        self.data_getters[name] = getter

    def log(self):
        if wpilib.DriverStation.getInstance().isDisabled() and not self.log_while_disabled:
            return
        if not self.header_logged:
            self.log_header()
        row = []
        t1 = self.timer.get()
        for key in self.data_getters.keys():
            row.append(self.data_getters[key]())
        t2 = self.timer.get()
        self.writer.writerow(row)
        t3 = self.timer.get()
        print("ts logs: %s %s" % (t2-t1, t3-t2))

    def log_header(self):
        self.writer.writerow(self.data_getters.keys())
        self.header_logged = True

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

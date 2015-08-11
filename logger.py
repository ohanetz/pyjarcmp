import os
import time


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        
    def log(self, msg):
        l = open(self.log_file, "a")
        l.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " " + msg + os.linesep)
        l.close()

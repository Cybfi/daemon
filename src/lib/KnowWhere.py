# KnowWhere lets the app know where to put things

import os
from platform import system
from pathlib import Path
from elevate import elevate
import sys

PLATFORM = system()


class KnowWhere:
    def __init__(self):
        self.platform: "Windows" or "Darwin" or "Linux" = PLATFORM
        self.home = os.path.expanduser("~")
        if self.platform == "Windows":
            self.appdata = os.getenv("APPDATA")
            self.localappdata = os.getenv("LOCALAPPDATA")
            self.temp = os.getenv("TEMP")
        elif self.platform == "Linux":
            self.appdata = Path("~/.config")
            self.localappdata = self.home
            self.temp = "/tmp"
        elif self.platform == "Darwin":
            self.appdata = Path("~/Library/Application Support")
            self.localappdata = self.home
            self.temp = os.getenv("TMPDIR")
                

        else:
            raise Exception("Unknown platform")
        # CREATE DIRECTORIES
        self.appdata = self.appdata + "/.cybfi"
        self.localappdata = self.localappdata + "/.cybfi"
        self.temp = self.temp + "/cybfi"
        for path in [self.appdata, self.localappdata, self.temp]:
            if not os.path.exists(path):
                try:
                    os.mkdir(path)
                except PermissionError as e:
                    print("Permission denied while creating directory " + path)
                    print("Elevating...")
                    elevate()
                    os.mkdir(path)

        # CREATE FILES
        self.STATUSOUT = self.temp + "/status.out"
        if not os.path.exists(self.STATUSOUT):
            open(self.STATUSOUT, "w").close()

        # CONSOLE
        self.STATUSOUT = self.temp + "/statusout"
        self.LOGOUT = sys.stdout

    def write_status(self, text):
        with open(self.STATUSOUT, "w") as f:
            f.write(text + "\r\n")

    def force_clean(self):
        for dir in [self.appdata, self.programdata, self.localappdata, self.temp]:
            if os.path.exists(dir):
                try:
                    os.rmdir(dir)
                except PermissionError as e:
                    print("Permission denied while deleting directory " + dir)
                    print("Elevating...")
                    elevate()
                    os.rmdir(dir)

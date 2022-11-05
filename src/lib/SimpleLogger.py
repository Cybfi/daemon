from typing import TextIO


class SimpleLogger:
    logOut: TextIO
    logLevel: int
    logLevelNames: dict[int, str]

    def __init__(self, logOut: TextIO, logLevel: int = 0) -> None:
        self.logOut = logOut
        self.logLevel = logLevel
        self.logLevelNames = {
            0: "INFO",
            1: "WARN",
            2: "ERROR",
        }

    def log(self, message: str, logLevel: int = 0) -> None:
        if logLevel >= self.logLevel:
            print(f"{self.logLevelNames[logLevel]}: {message}", file=self.logOut)

    def info(self, message: str) -> None:
        self.log(message, 0)

    def warn(self, message: str) -> None:
        self.log(message, 1)

    def error(self, message: str) -> None:
        self.log(message, 2)

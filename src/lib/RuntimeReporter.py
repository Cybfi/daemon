import uuid

from lib.GlobalManager import gmget
from lib.SimpleLogger import SimpleLogger

_LOGGER: SimpleLogger = gmget("logger")

class RuntimeReporter:
    def __init__(self, uuid: str = uuid.uuid4()):
        self.uuid = uuid

    def report(self, message: str):
        _LOGGER.info(f"Reported: {message}")

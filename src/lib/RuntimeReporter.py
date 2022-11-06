import uuid


class RuntimeReporter:
    def __init__(self, uuid: str = uuid.uuid4()):
        self.uuid = uuid

    def report(self, message: str):
        print("PLACEHOLDER: REPORT: " + message)

import os, time


class WordList:
    remote: str
    local: str

    def __init__(self, remote: str, local: str):
        self.remote = remote
        self.local = local

    def download(self):
        import requests
        with open(self.local, "w") as file:
            file.write(requests.get(self.remote).text)

    def fetch(self) -> bool:
        if not os.path.exists(self.local):
            self.download()
            return True
        return False

    def check(self, text: str) -> bool:
        with open(self.local) as file:
            for word in file.readlines():
                if word in text:
                    return True
        return False

    def decayed_fetch(self, s: float):
        # if file is older than s seconds, fetch
        if not os.path.exists(self.local):
            self.download()
            return True
        if time.time() - os.path.getctime(self.local) > s:
            self.download()
            return True
        return False

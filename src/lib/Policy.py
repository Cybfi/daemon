from threading import Thread


class Policy:
    def __init__(self):
        self.active = False
        self.thread: Thread = None

    def start(self, create_thread: bool = True) -> Thread or None:
        """ Start the policy """
        self.active = True
        if create_thread:
            self.thread = Thread(target=self._THR_FUNC)
            self.thread.start()
            return self.thread
        return None

    def stop(self):
        """ Stop the policy """
        self.active = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        pass

    def _THR_FUNC(self):
        """ Thread function """
        pass

    def __str__(self):
        return f"Policy: {self.constructor.__name__} - Active: {self.active}"

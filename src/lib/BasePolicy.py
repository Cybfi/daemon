from typing import Callable


class BasePolicy:
    def __init__(self, name: str, thr_func: Callable):
        self.name = name
        self.thr_func = thr_func

    def __str__(self):
        return self.name
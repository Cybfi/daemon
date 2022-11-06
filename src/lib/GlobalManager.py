class GlobalItem:
    name: str
    value: any

    def __init__(self, name: str, value: any):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} = {self.value}"


_GM_CACHE: dict[str, GlobalItem] = {}


def gmset(name: str, value: any) -> any:
    _GM_CACHE[name] = GlobalItem(name, value)
    return value


def gmget(name: str) -> any:
    return _GM_CACHE.get(name, GlobalItem("NONE", None)).value

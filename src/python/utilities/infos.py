from typing import Any


def log(section: str, message: str, *parameters: Any) -> None:
    formatted = "[{}] {}".format(section, message.format(*parameters))
    print(formatted)

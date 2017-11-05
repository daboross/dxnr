from typing import Any, NewType

from defs import *

LogLevel = NewType("LogLevel", int)

error = LogLevel(4)
warning = LogLevel(3)
info = LogLevel(2)
debug = LogLevel(1)
trace = LogLevel(0)

enabled_level = debug
enabled_notify_level = error


def describe_level(level: LogLevel) -> str:
    if level == trace:
        return "trace"
    elif level == debug:
        return "debug"
    elif level == info:
        return "info"
    elif level == warning:
        return "warning"
    elif level == error:
        return "error"
    else:
        return str(level)


def log(level: LogLevel, section: str, message: str, *parameters: Any) -> None:
    if level < enabled_level:
        return
    formatted = "[{}][{}] {}".format(describe_level(level), section, message.format(*parameters))
    print(formatted)
    if level >= enabled_notify_level:
        Game.notify(formatted)


class Log:
    def __init__(self, section: str) -> None:
        self.section = section

    def log(self, level: LogLevel, message: str, *parameters: Any) -> None:
        log(level, self.section, message, *parameters)

    def trace(self, message: str, *parameters: Any) -> None:
        self.log(trace, message, *parameters)

    def debug(self, message: str, *parameters: Any) -> None:
        self.log(debug, message, *parameters)

    def info(self, message: str, *parameters: Any) -> None:
        self.log(info, message, *parameters)

    def warning(self, message: str, *parameters: Any) -> None:
        self.log(warning, message, *parameters)

    def error(self, message: str, *parameters: Any) -> None:
        self.log(error, message, *parameters)

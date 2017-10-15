from typing import NewType

from constants import TaskId
from defs import *

TaskTypeId = NewType("TaskTypeId", int)


class Schedule:
    def __init__(self) -> None:
        pass

    def matches(self, task_id: TaskId) -> bool:
        pass

    @staticmethod
    def every_ticks(ticks: int) -> 'Schedule':
        return EveryTicks(ticks)

    @staticmethod
    def always() -> 'Schedule':
        return Always()


class EveryTicks(Schedule):
    def __init__(self, ticks: int) -> None:
        Schedule.__init__(self)
        self.repeat_every_ticks = ticks

    def matches(self, task_id: TaskId) -> bool:
        return Game.time % self.repeat_every_ticks == (task_id % 50)


class Always(Schedule):
    def __init__(self) -> None:
        Schedule.__init__(self)

    def matches(self, task_id: TaskId) -> bool:
        return True

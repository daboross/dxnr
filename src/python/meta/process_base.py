from typing import List, TYPE_CHECKING

from constants import ProcessId
from defs import *
from meta.tasks import Schedule

if TYPE_CHECKING:
    from core.kernel import Kernel


class Process:
    def __init__(self, pid: ProcessId, kernel: Kernel):
        """
        Creates an instance of this process using the given kernel.

        Can be definitively overwritten with
        """
        self.pid = pid
        self.kernel = kernel

    # TOOD: Kernel overwriting feature and caching

    def run(self):
        pass

    def should_run(self):
        return True


class HasMemory(Process):
    def memory(self):
        return self.kernel.process_memory(self.pid)


class HasCreeps(Process, HasMemory):
    def creeps(self) -> List[Creep]:
        pass

    def claim_spawned_creep(self, name: str) -> None:
        pass



class Infrequent(Process):
    frequency = Schedule.always()

    def should_run(self):
        return self.frequency.matches(self.pid)

from typing import Any, Dict, List, Optional, TYPE_CHECKING, cast

from constants import InnerProcessMemKey, ProcessId, ProcessTypeId
from defs import *
from meta.tasks import Schedule
from utilities import creep_memory

if TYPE_CHECKING:
    from core.kernel import Kernel

punified_mkey_owned_creeps = InnerProcessMemKey("c")
punified_mkey_home = InnerProcessMemKey("h")


class Process:
    ptid = None  # type: ProcessTypeId

    def __init__(self, pid: ProcessId, kernel: Kernel) -> None:
        """
        Creates an instance of this process using the given kernel.
        """
        self.pid = pid
        self.kernel = kernel

    def init(self, *parameters: Any) -> None:
        pass

    def run(self) -> None:
        pass

    def should_run(self) -> bool:
        return True

    def child_died(self, child_pid: ProcessId, child_ptid: ProcessTypeId) -> None:
        pass

    def died(self) -> None:
        pass


class HasMemory(Process):
    def memory(self) -> Dict[InnerProcessMemKey, Any]:
        return self.kernel.process_memory(self.pid)


# TODO: more complicated stuff here...
class CreepSpawnInfo:
    def __init__(self, pid: ProcessId, base: List[str]) -> None:
        self.pid = pid
        self.base = base

    def serialize(self) -> Any:
        return self

    @staticmethod
    def deserialize(memory: Any) -> 'CreepSpawnInfo':
        return memory

    def toString(self) -> str:
        return "CreepSpawnInfo[pid: {}, base: {}]".format(self.pid, self.base)


class HasCreeps(HasMemory, Process):
    def creeps(self) -> List[Creep]:
        mem = self.memory()
        if punified_mkey_owned_creeps in mem:
            result = []
            dead = None
            creeps = mem[punified_mkey_owned_creeps]
            for index in range(0, len(creeps)):
                name = creeps[index]
                creep = Game.creeps[name]
                if creep:
                    result.append(creep)
                else:
                    # TODO: death notice?
                    if dead is None:
                        dead = [index]
                    else:
                        dead.append(index)
            if dead is not None:
                for index in dead:
                    name = creeps[index]
                    creep_memory.clean_screeps_creep_memory(name)
                _.pullAt(mem[punified_mkey_owned_creeps], dead)

            return _.map(mem[punified_mkey_owned_creeps], lambda n: Game.creeps[n])
        else:
            return []

    def claim_spawned_creep(self, name: str) -> None:
        mem = self.memory()
        if punified_mkey_owned_creeps in mem:
            mem[punified_mkey_owned_creeps].append(name)
        else:
            mem[punified_mkey_owned_creeps] = [name]

    def get_needed_creep(self) -> Optional[CreepSpawnInfo]:
        return None

    def get_next_expire(self) -> int:
        min_life = CREEP_LIFE_TIME
        for creep in self.creeps():
            min_life = min(min_life, creep.ticksToLive)
        return Game.time + min_life


class Infrequent(Process):
    frequency = Schedule.always()

    def should_run(self) -> bool:
        return self.frequency.matches(self.pid)


class HasHome(HasMemory, Process):
    def __init__(self, pid: ProcessId, kernel: Kernel) -> None:
        Process.__init__(self, pid, kernel)

    def init(self, *parameters: Any) -> None:
        self.set_owned_room(cast(str, parameters[0]))

    def set_owned_room(self, room: str) -> None:
        self.memory()[punified_mkey_home] = room

    def room_name(self) -> str:
        return self.memory()[punified_mkey_home]

    def room(self) -> Room:
        room = Game.rooms[self.memory()[punified_mkey_home]]
        if not room:
            raise ValueError("process {} has no home.".format(self.pid))
        return room

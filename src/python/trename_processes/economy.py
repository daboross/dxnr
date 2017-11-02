from typing import TYPE_CHECKING

from constants import InnerProcessMemKey, ProcessId
from constants.processes import mtid_startup, ptid_economy, ptid_upgrading_level1
from core.process_type import ProcessType
from defs import *
from meta.registry_exports import Exports
from utilities import infos, warnings

if TYPE_CHECKING:
    # TODO: make Transcrypt ignore type-only imports
    from core.kernel import Kernel

key_room_we_own = InnerProcessMemKey("r")
key_mining_process_pid = InnerProcessMemKey("m")

section = "process: economy"


def run(pid: ProcessId, kernel: Kernel) -> None:
    mem = kernel.process_memory(pid)
    room_name = mem[key_room_we_own]
    us = Game.rooms[room_name]
    if not us:
        warnings.process_failure_exiting(ptid_economy, "can't see {}", room_name)
        kernel.kill(pid)
        return

    kernel.get_or_spawn_child(pid, ptid_upgrading_level1)

def start(pid: ProcessId, kernel: Kernel, from_pid: ProcessId, room_name: str) -> None:
    kernel.process_memory(pid)[key_room_we_own] = room_name


exports = Exports().process(ProcessType(ptid_economy, run).message(mtid_startup, start))

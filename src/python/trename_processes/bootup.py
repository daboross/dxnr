from typing import TYPE_CHECKING

from constants import ProcessId
from constants.processes import mtid_startup, ptid_bootup, ptid_economy

from core.process_type import ProcessType
from defs import *
from meta.registry_exports import Exports
from utilities import infos

if TYPE_CHECKING:
    # TODO: make Transcrypt ignore type-only imports
    from core.kernel import Kernel

section = "process: bootup"

def run(pid: ProcessId, kernel: Kernel) -> None:
    my_rooms = _.filter(Game.rooms, {'controller': {'my': True}})
    if not len(my_rooms):
        infos.log(section, "no rooms?")
        return

    infos.log(section, "booting up")
    for room in my_rooms:
        new_pid = kernel.spawn(pid, ptid_economy)
        kernel.message(pid, mtid_startup, new_pid, room.name)

    kernel.kill(pid)


exports = Exports().process(ProcessType(ptid_bootup, run))

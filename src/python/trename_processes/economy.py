from typing import TYPE_CHECKING

from constants import InnerProcessMemKey, ProcessId, ProcessTypeId
from constants.processes import ptid_economy, ptid_spawning, ptid_upgrading_level1
from meta.process_base import HasHome
from meta.registry_exports import Exports
from utilities import warnings
from utilities.infos import Log

if TYPE_CHECKING:
    # TODO: make Transcrypt ignore type-only imports
    pass

key_current_upgrade_process_pid = InnerProcessMemKey("m")
key_current_spawning_process_pid = InnerProcessMemKey("p")

log = Log("process: economy")


class Econ(HasHome):
    ptid = ptid_economy

    def run(self) -> None:
        our_room = self.room()
        if our_room is None:
            warnings.process_failure_exiting(ptid_economy, "can't see {}", self.room())
            self.kernel.kill(self.pid)
            return

        if key_current_upgrade_process_pid not in self.memory():
            upgrade_pid = self.kernel.spawn(self.pid, ptid_upgrading_level1, our_room.name)
            self.memory()[key_current_upgrade_process_pid] = upgrade_pid
        if key_current_spawning_process_pid not in self.memory():
            spawning_pid = self.kernel.spawn(self.pid, ptid_spawning, our_room.name)
            self.memory()[key_current_spawning_process_pid] = spawning_pid

    def child_died(self, child_pid: ProcessId, child_ptid: ProcessTypeId) -> None:
        mem = self.memory()
        if child_pid is mem[key_current_upgrade_process_pid]:
            del mem[key_current_upgrade_process_pid]
        if child_pid is mem[key_current_spawning_process_pid]:
            del mem[key_current_spawning_process_pid]


exports = Exports().process(Econ)

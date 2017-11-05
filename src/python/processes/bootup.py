from typing import TYPE_CHECKING

from constants.processes import ptid_bootup, ptid_economy, ptid_root
from defs import *
from meta.process_base import Process
from meta.registry_exports import Exports
from utilities.infos import Log

if TYPE_CHECKING:
    # TODO: make Transcrypt ignore type-only imports
    pass

log = Log("process: bootup")


class Bootup(Process):
    ptid = ptid_bootup

    def run(self) -> None:
        my_rooms = _.filter(Game.rooms, {'controller': {'my': True}})
        if not len(my_rooms):
            log.warning("no rooms found")
            return

        log.info("booting up")

        log.info("starting root")
        root_pid = self.kernel.spawn(None, ptid_root)

        for room in my_rooms:
            log.debug("booting room {}", room.name)
            self.kernel.spawn(root_pid, ptid_economy, room.name)

        self.kernel.kill(self.pid)


class Root(Process):
    ptid = ptid_root


exports = Exports().process(Bootup).process(Root)

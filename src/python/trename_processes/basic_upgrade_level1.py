from typing import List, Optional, cast

from constants.memkeys import key_creep_filling
from constants.processes import ptid_upgrading_level1
from constants.targets import target_source
from defs import *
from meta.process_base import CreepSpawnInfo, HasCreeps, HasHome
from meta.registry_exports import Exports
from providers import targets
from providers.movement import standard_move
from utilities.infos import Log

log = Log("process: upgrade1")


class BasicUpgradeLvl1(HasHome, HasCreeps):
    ptid = ptid_upgrading_level1

    def run(self) -> None:
        creeps = self.creeps()
        room = self.room()
        for creep in creeps:
            run_creep(room, creep)

    def get_needed_creep(self) -> Optional[CreepSpawnInfo]:
        creeps = self.creeps()
        if len(creeps) < 8:
            log.trace("get_needed_creep: returning that we do need a creep")
            return CreepSpawnInfo(self.pid, [WORK, CARRY, MOVE, MOVE])
        else:
            log.trace("get_needed_creep: returning that we're a-ok")
            return None


def run_creep(room: Room, creep: Creep) -> None:
    # Basic upgrader class. TODO: smart room management
    if creep.spawning:
        return

    if creep.carryCapacity <= 0 or not creep.getActiveBodyparts(WORK):
        return

    memory = creep.memory

    if memory[key_creep_filling]:
        if _.sum(creep.carry) >= creep.carryCapacity:
            memory[key_creep_filling] = False
            targets.unregister_target(creep, target_source)
    else:
        if _.sum(creep.carry) <= 0:
            memory[key_creep_filling] = True

    if memory[key_creep_filling]:
        source = cast(Source, targets.get_or_find_target(creep, target_source))
        if source:
            if creep.pos.isNearTo(source):
                creep.harvest(source)
            else:
                standard_move.move_to(creep, source.pos)
    else:
        controller = room.controller
        if creep.pos.inRangeTo(controller, 3):
            creep.upgradeController(controller)
        if not creep.pos.isNearTo(controller):
            standard_move.move_to(creep, controller.pos)


def find_source(creep: Creep) -> Optional[str]:
    best_source = None
    least_used_amount = Infinity
    for source in cast(List[Source], creep.room.find(FIND_SOURCES_ACTIVE)):
        used_here = targets.get_number_of_targeters(target_source, source.id)
        if used_here < least_used_amount:
            least_used_amount = used_here
            best_source = source
    if best_source:
        return best_source.id
    else:
        return None


exports = (
    Exports()
        .process(BasicUpgradeLvl1)
        .target(target_source, find_source)
)

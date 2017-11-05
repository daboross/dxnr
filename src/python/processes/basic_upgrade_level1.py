from typing import List, Optional, cast

from constants.memkeys import key_creep_filling
from constants.processes import ptid_upgrading_level1
from constants.targets import target_source, target_spawn_fill
from defs import *
from meta.process_base import CreepSpawnInfo, HasCreeps, HasHome
from meta.registry_exports import Exports
from providers import targets
from providers.movement import standard_move
from utilities import world
from utilities.infos import Log

log = Log("process: upgrade1")


def incapacitated(creep: Creep) -> bool:
    return creep.carryCapacity <= 0 or not creep.getActiveBodyparts(WORK)


class BasicUpgradeLvl1(HasHome, HasCreeps):
    ptid = ptid_upgrading_level1

    def run(self) -> None:
        creeps = self.creeps()
        room = self.room()
        need_spawn_filling = len(creeps) < 8 and room.energyAvailable < room.energyCapacityAvailable

        for creep in creeps:
            if creep.spawning:
                continue
            if incapacitated(creep):
                log.info("creep incapacitated: killing {}", creep)
                creep.suicide()
                continue

            if fill_creep(creep):
                continue

            if need_spawn_filling:
                spawn_fill(creep)
            else:
                upgrade(room, creep)

    def get_needed_creep(self) -> Optional[CreepSpawnInfo]:
        creeps = self.creeps()
        if len(creeps) < 8:
            log.trace("get_needed_creep: returning that we do need a creep")
            return CreepSpawnInfo(self.pid, [WORK, CARRY, MOVE, MOVE])
        else:
            log.trace("get_needed_creep: returning that we're a-ok")
            return None


def fill_creep(creep: Creep) -> bool:
    if creep.memory[key_creep_filling]:
        if _.sum(creep.carry) >= creep.carryCapacity:
            del creep.memory[key_creep_filling]
            targets.unregister_target(creep, target_source)
            return False
    else:
        if creep.carry[RESOURCE_ENERGY] <= 0:
            creep.memory[key_creep_filling] = True
        else:
            return False

    source = cast(Source, targets.get_or_find_target(creep, target_source))
    if source:
        if creep.pos.isNearTo(source):
            creep.harvest(source)
        else:
            standard_move.move_to(creep, source.pos)
    return True


def upgrade(room: Room, creep: Creep) -> None:
    controller = room.controller
    if creep.pos.inRangeTo(controller, 3):
        creep.upgradeController(controller)
    if not creep.pos.isNearTo(controller):
        standard_move.move_to(creep, controller.pos)


def spawn_fill(creep: Creep) -> None:
    spawn = cast(StructureSpawn, targets.get_or_find_target(creep, target_spawn_fill))
    if spawn:
        if spawn.energy >= spawn.energyCapacity:
            targets.unregister_target(creep, target_spawn_fill)
        else:
            if creep.pos.isNearTo(spawn):
                creep.transfer(spawn, RESOURCE_ENERGY)
            else:
                standard_move.move_to(creep, spawn.pos)
            return


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


def find_spawn(creep: Creep) -> Optional[str]:
    best = None
    closest_empty = Infinity
    for spawn_name in Object.keys(Game.spawns):
        spawn = Game.spawns[spawn_name]
        if spawn.energy < spawn.energyCapacity:
            distance = world.distance(creep.pos, spawn.pos)
            if distance < closest_empty:
                closest_empty = distance
                best = spawn
    if best:
        return best.id
    else:
        return None


exports = (
    Exports()
        .process(BasicUpgradeLvl1)
        .target(target_source, find_source)
        .target(target_spawn_fill, find_spawn)
)

from typing import Dict, List, Optional, cast

from constants import SpawnIdeaKey
from constants.memkeys import key_creep_filling
from constants.roles import role_upgrader
from constants.spawning import body_type_upgrader, spawn_idea_key_body, spawn_idea_key_role, spawn_idea_key_size, \
    spawn_priority_upgrader
from constants.targets import target_source
from defs import *
from meta.registry_exports import Exports
from providers import exp_memory, targets


def run(room: Room, creep: Creep) -> None:
    # Basic upgrader class. TODO: smart room management
    if creep.spawning:
        return

    if creep.carryCapacity <= 0 or not creep.getActiveBodyparts(WORK):
        return

    memory = exp_memory.creep_mem(creep.name)

    if memory[key_creep_filling]:
        if _.sum(creep.carry) >= creep.carryCapacity:
            memory[key_creep_filling] = False
    else:
        if _.sum(creep.carry) <= 0:
            memory[key_creep_filling] = True

    if memory[key_creep_filling]:
        source = cast(Source, targets.get_or_find_target(creep, target_source))
        if source:
            if creep.pos.isNearTo(source):
                creep.harvest(source)
            else:
                creep.moveTo(source)
    else:
        controller = room.controller
        if creep.pos.inRangeTo(controller, 3):
            creep.upgradeController(controller)
        if not creep.pos.isNearTo(controller):
            creep.moveTo(controller)


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


def spawn_need(room: Room) -> Optional[Dict[SpawnIdeaKey, int]]:
    # we always need upgrader creeps, of course!
    return {
        spawn_idea_key_role: role_upgrader,
        spawn_idea_key_body: body_type_upgrader,
        spawn_idea_key_size: 1,
    }


exports = (
    Exports()
        .role(role_upgrader, run)
        .target(target_source, find_source)
        .spawning_need(spawn_priority_upgrader, spawn_need)
)

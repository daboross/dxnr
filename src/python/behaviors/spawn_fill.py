from typing import Dict, Optional, cast

from constants import SpawnIdeaKey
from constants.memkeys import key_creep_filling, key_creep_role
from constants.roles import role_spawn_fill
from constants.spawning import body_type_upgrader, spawn_idea_key_body, spawn_idea_key_role, spawn_idea_key_size, \
    spawn_priority_spawn_fill
from constants.targets import target_source, target_spawn_fill
from defs import *
from meta.registry_exports import Exports
from providers import exp_memory, targets
from providers.movement import standard_move
from utilities import world


def spawn_fill(room: Room, creep: Creep) -> None:
    # TODO: room specific logic

    if creep.spawning:
        return

    if creep.carryCapacity <= 0 or not creep.getActiveBodyparts(WORK):
        return

    memory = exp_memory.creep_mem(creep.name)

    if memory[key_creep_filling]:
        if _.sum(creep.carry) >= creep.carryCapacity:
            memory[key_creep_filling] = False
            targets.unregister_target(creep, target_source)
    else:
        if creep.carry[RESOURCE_ENERGY] <= 0:
            memory[key_creep_filling] = True
            targets.unregister_target(creep, target_spawn_fill)

    if memory[key_creep_filling]:
        source = cast(Source, targets.get_or_find_target(creep, target_source))
        if source:
            if creep.pos.isNearTo(source):
                creep.harvest(source)
            else:
                standard_move.move_to(creep, source.pos)
    else:
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

        controller = room.controller
        if creep.pos.inRangeTo(controller, 3):
            creep.upgradeController(controller)
        if not creep.pos.isNearTo(controller):
            standard_move.move_to(creep, controller.pos)


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


def spawn_need(room: Room) -> Optional[Dict[SpawnIdeaKey, int]]:
    # TODO: room-level knowledge of this that's pre calculated
    creeps = _.sum(Game.creeps, lambda c: exp_memory.creep_mem_ro(c.name)[key_creep_role] == role_spawn_fill)
    if creeps < 4:
        return {
            spawn_idea_key_role: role_spawn_fill,
            spawn_idea_key_body: body_type_upgrader,
            spawn_idea_key_size: 1,
        }
    else:
        return None


exports = (
    Exports()
        .role(role_spawn_fill, spawn_fill)
        .target(target_spawn_fill, find_spawn)
        .spawning_need(spawn_priority_spawn_fill, spawn_need)
)

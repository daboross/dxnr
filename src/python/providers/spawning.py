from typing import Dict, List, cast

from constants import BodyTypeId, RoleId
from constants.memkeys import key_creep_role
from constants.spawning import body_type_upgrader, spawn_idea_key_body, spawn_idea_key_role, spawn_idea_key_size
from defs import *
from providers import exp_memory, registry
from utilities import errors, names

# TODO: generify
bodies = {
    body_type_upgrader: {
        1: [WORK, CARRY, MOVE, MOVE],
    }
}
costs = {}  # type: Dict[BodyTypeId, Dict[int, int]]


def _init_costs() -> None:
    for body_type in Object.keys(bodies):
        costs[body_type] = {}
        this_type_bodies = bodies[body_type]
        for size in Object.keys(this_type_bodies):
            costs[body_type][size] = _.sum(this_type_bodies[size], lambda part: BODYPART_COST[part])


_init_costs()


@errors.catching(lambda spawn: "running spawn {}".format(spawn))
def run_spawn(spawn: StructureSpawn) -> None:
    if spawn.spawning:
        return

    room = spawn.room

    for _priority, callback in registry.get().ordered_spawn_possibilities:
        spawn_idea = callback(room)
        if spawn_idea:
            # TODO: handle errors here
            # TODO: spawn_idea should be a typed structure...
            body_type = cast(BodyTypeId, spawn_idea[spawn_idea_key_body])
            role_id = cast(RoleId, spawn_idea[spawn_idea_key_role])
            body_size = spawn_idea[spawn_idea_key_size]
            if body_size == undefined:
                body_size = 1
            body = bodies[body_type][body_size]
            cost = costs[body_type][body_size]

            if spawn.room.energyAvailable >= cost:
                _do_spawn(spawn, body, role_id)
            break


def _do_spawn(spawn: StructureSpawn, body: List[str], role: RoleId) -> None:
    name = names.create_name_excluding_keys_to(Game.creeps)
    exp_memory.creep_mem(name)[key_creep_role] = role
    spawn.createCreep(body, name)  # TODO: check result

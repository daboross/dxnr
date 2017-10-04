from constants.memkeys import key_creep_role
from constants.roles import role_upgrader
from defs import *

from utilities import errors


@errors.catching(lambda spawn: "running spawn {}".format(spawn))
def run_spawn(spawn: StructureSpawn):
    if spawn.spawning:
        return

    body = [WORK, CARRY, MOVE, MOVE]
    cost = _.sum(body, lambda part: BODYPART_COST[part])

    if spawn.room.energyAvailable >= cost:
        spawn.createCreep(body, None, {key_creep_role: role_upgrader})

import behaviors
import providers
from defs import *
from providers import roles, spawning
from utilities import errors

behaviors.register()


@errors.catching(lambda: "running main")
def main():
    """
    Main game logic loop.
    """

    providers.instantiate()

    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.room.controller and creep.room.controller.my:
            room = creep.room
        else:
            room = _.find(Game.structures).room
        roles.run_creep(room, creep)

    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        spawning.run_spawn(spawn)


module.exports.loop = main

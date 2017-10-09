import behaviors
import providers
import tasks
from defs import *
from providers import registry, roles, spawning
from utilities import errors

behaviors.register()
tasks.register()
registry.finalize()


@errors.catching(lambda: "running main")
def main() -> None:
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

    for task_id, schedule, callback in registry.get().empire_tasks:
        if schedule.matches(task_id):
            errors.execute_catching(callback, lambda: "task {}".format(task_id))
    pass
    # TODO: room tasks here


module.exports.loop = main

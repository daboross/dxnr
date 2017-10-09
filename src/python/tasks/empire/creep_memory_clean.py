from constants.memkeys import key_memory_creeps
from constants.tasks import empire_task, task_clear_memory, task_clear_memory_deep
from defs import *
from meta.registry_exports import Exports
from meta.tasks import Schedule
from providers import exp_memory, targets


def clean_creep_memory() -> None:
    if 'creeps' in Memory:
        for name in Object.keys(Memory.creeps):
            if name not in Game.creeps:
                del Memory.creeps[name]
    creep_mem = exp_memory.top_level_mem(key_memory_creeps)
    for name in Object.keys(creep_mem):
        if name not in Game.creeps:
            del creep_mem[name]
            targets.unregister_all(name)


def deep_clean_targets() -> None:
    for name in targets.all_registered_creeps():
        if name not in Game.creeps:
            targets.unregister_all(name)


exports = Exports().task(
    empire_task,
    task_clear_memory,
    Schedule.every_ticks(100),
    clean_creep_memory,
).task(
    empire_task,
    task_clear_memory_deep,
    Schedule.every_ticks(2000),
    deep_clean_targets,
)

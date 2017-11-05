from defs import *

top_level_key_creeps = "creeps"


def clean_screeps_creep_memory(name: str) -> None:
    if Memory[top_level_key_creeps]:
        del Memory[top_level_key_creeps][name]
        if _.isEmpty(Memory[top_level_key_creeps]):
            del Memory[top_level_key_creeps]

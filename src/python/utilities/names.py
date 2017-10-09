from constants.memkeys import key_memory_creeps
from defs import *
from providers import exp_memory


def create_name_excluding_existing() -> str:
    name = _random_name()
    all_creeps = exp_memory.top_level_mem_ro(key_memory_creeps)
    while name in all_creeps:
        name += _random_name()
    return name


def _random_name() -> str:
    num = 40 + _.random(0, 85)
    if num > 91:
        num += 1  # skip 92
    return String.fromCodePoint(num)

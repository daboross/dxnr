from constants.memkeys import key_creep_role
from defs import *
from providers import exp_memory
from utilities import warnings


def move_to(creep: Creep, target: RoomPosition) -> int:
    result = creep.moveTo(target, {
        'ignoreCreeps': True,
    })
    if result == ERR_NO_PATH:
        result = creep.moveTo(target, {
            'ignoreCreeps': False,
        })

    if result != OK and result != ERR_TIRED:
        warnings.warn("unknown result from (creep {}, role: {}).moveTo({}): {}"
                      .format(creep.name, exp_memory.creep_mem_ro(creep.name)[key_creep_role], target,
                              warnings.transform_error_code(result)))

    return result

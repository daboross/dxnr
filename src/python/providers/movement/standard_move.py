from defs import *
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
        warnings.warn("unknown result from (creep {}).moveTo({}): {}"
                      .format(creep.name, target, warnings.transform_error_code(result)))

    return result

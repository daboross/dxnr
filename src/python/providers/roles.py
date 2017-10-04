from typing import Callable, Optional

from constants.memkeys import key_creep_role
from defs import *
from providers import registry
from utilities import errors, warnings


def get_role_func(creep: Creep) -> Optional[Callable[[Room, Creep], None]]:
    role_funcs = registry.get().role_type_to_run_function
    role = creep.memory[key_creep_role]
    if role and role in role_funcs:
        return role_funcs[role]

    warnings.missing_registration("creep", role)
    return None


@errors.catching(lambda room, creep:
                 "running creep {} (role: {}, room: {})"
                 .format(creep, creep.memory[key_creep_role], room))
def run_creep(room: Room, creep: Creep) -> None:
    run_func = get_role_func(creep)
    if run_func:
        run_func(room, creep)

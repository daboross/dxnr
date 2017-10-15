from typing import Callable, Optional

from constants.memkeys import key_creep_role
from defs import *
from providers import exp_memory, registry
from utilities import errors, warnings


def get_role_func(creep: Creep) -> Optional[Callable[[Room, Creep], None]]:
    role_funcs = registry.get().role_type_to_run_function
    role = exp_memory.creep_mem_ro(creep.name)[key_creep_role]
    if role and role in role_funcs:
        return role_funcs[role]

    warnings.missing_registration("creep", role)
    return None


def _run_creep_desc(room: Room, creep: Creep) -> str:
    return ("running creep {} (role: {}, room: {})"
            .format(creep, exp_memory.creep_mem_ro(creep.name)[key_creep_role], room))


@errors.catching(_run_creep_desc)
def run_creep(room: Room, creep: Creep) -> None:
    run_func = get_role_func(creep)
    if run_func:
        run_func(room, creep)

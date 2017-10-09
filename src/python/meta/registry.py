from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Tuple

from constants import RoleId, SpawnIdeaKey, SpawnPriorityId, TargetTypeId
from defs import *
from utilities import warnings

if TYPE_CHECKING:
    from .registry_exports import Exports


class Database:
    def __init__(self) -> None:
        self.target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self.role_type_to_run_function = {}  # type: Dict[RoleId, Callable[[Room, Creep], None]]
        self.ordered_spawn_possibilities = []  # type: List[Tuple[SpawnPriorityId, Callable[[Room], Optional[Dict[SpawnIdeaKey, int]]]]]

    def register(self, exports: Exports) -> 'Database':
        target_functions_to_register = exports.get_exported_target_functions()
        for target_type in Object.keys(target_functions_to_register):
            if target_type in self.target_type_to_find_function:
                warnings.repeated_registration("target", target_type)
            self.target_type_to_find_function[target_type] = target_functions_to_register[target_type]
        role_functions_to_register = exports.get_exported_role_functions()
        for role_type in Object.keys(role_functions_to_register):
            if role_type in self.role_type_to_run_function:
                warnings.repeated_registration("role", role_type)
            self.role_type_to_run_function[role_type] = role_functions_to_register[role_type]
        for spawn_tuple in exports.get_exported_spawn_needs():
            self.ordered_spawn_possibilities.append(spawn_tuple)
        return self

    def finalize(self) -> None:
        self.ordered_spawn_possibilities = _.sortBy(
            _.shuffle(self.ordered_spawn_possibilities),
            lambda t: t[0]
        )

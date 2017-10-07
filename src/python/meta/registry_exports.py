from typing import Callable, Dict, Optional

from constants import RoleId, TargetTypeId
from defs import *
from utilities import warnings


class Exports:
    def __init__(self) -> None:
        self._target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self._role_type_to_run_function = {}  # type: Dict[RoleId, Callable[[Room, Creep], None]]

    def role(self, role_type: RoleId, callback: Callable[[Room, Creep], None]) -> 'Exports':
        if role_type in self._role_type_to_run_function:
            warnings.repeated_registration("role", role_type)
        self._role_type_to_run_function[role_type] = callback
        return self

    def target(self, target_type: TargetTypeId, callback: Callable[[Creep], str]) -> 'Exports':
        if target_type in self._target_type_to_find_function:
            warnings.repeated_registration("target", target_type)
        self._target_type_to_find_function[target_type] = callback
        return self

    def room_task(self, task_id: int, callback: Callable[[Room], None]) -> 'Exports':
        # TODO: this
        return self

    def get_exported_target_functions(self) -> Dict[TargetTypeId, Callable[[Creep], Optional[str]]]:
        return self._target_type_to_find_function

    def get_exported_role_functions(self) -> Dict[RoleId, Callable[[Room, Creep], None]]:
        return self._role_type_to_run_function

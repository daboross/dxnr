from typing import Callable, Dict, Optional

from defs import *
from utilities import warnings


class Exports:
    def __init__(self) -> None:
        self._target_type_to_find_function = {}  # type: Dict[int, Callable[[Creep], Optional[str]]]
        self._role_type_to_run_function = {}  # type: Dict[int, Callable[[Room, Creep], None]]

    def role(self, role_type: int, callback: Callable[[Room, Creep], None]) -> 'Exports':
        if role_type in self._role_type_to_run_function:
            warnings.repeated_registration("role", role_type)
        self._role_type_to_run_function[role_type] = callback
        return self

    def target(self, target_type: int, callback: Callable[[Creep], str]) -> 'Exports':
        if target_type in self._target_type_to_find_function:
            warnings.repeated_registration("target", target_type)
        self._target_type_to_find_function[target_type] = callback
        return self

    def get_exported_target_functions(self) -> Dict[int, Callable[[Creep], Optional[str]]]:
        return self._target_type_to_find_function

    def get_exported_role_functions(self) -> Dict[int, Callable[[Room, Creep], None]]:
        return self._role_type_to_run_function

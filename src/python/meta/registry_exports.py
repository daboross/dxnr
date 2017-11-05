from typing import Callable, Dict, List, Optional, Type

from constants import TargetTypeId
from defs import *
from meta.process_base import Process
from utilities import warnings


class Exports:
    def __init__(self) -> None:
        self._target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self._process_types = []  # type: List[Type[Process]]

    def target(self, target_type: TargetTypeId, callback: Callable[[Creep], str]) -> 'Exports':
        if target_type in self._target_type_to_find_function:
            warnings.repeated_registration("target", target_type)
        self._target_type_to_find_function[target_type] = callback
        return self

    def process(self, process: Type[Process]) -> 'Exports':
        self._process_types.append(process)
        return self

    def get_exported_target_functions(self) -> Dict[TargetTypeId, Callable[[Creep], Optional[str]]]:
        return self._target_type_to_find_function

    def get_exported_processes(self) -> List[Type[Process]]:
        return self._process_types

    def merge(self, other: 'Exports') -> 'Exports':
        """
        Merges another exports into this exports.
        """
        for target_type_id in Object.keys(other._target_type_to_find_function):
            self.target(target_type_id, other._target_type_to_find_function[target_type_id])
        for type_tuple in other._process_types:
            self._process_types.append(type_tuple)
        return self

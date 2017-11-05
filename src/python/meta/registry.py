from typing import Callable, Dict, Optional, TYPE_CHECKING, Type

from constants import ProcessTypeId, TargetTypeId
from defs import *
from meta.process_base import Process
from utilities import warnings

if TYPE_CHECKING:
    from .registry_exports import Exports


class Database:
    def __init__(self) -> None:
        self.target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self.process_types = {}  # type: Dict[ProcessTypeId, Type[Process]]

    def register(self, exports: Exports) -> 'Database':
        for process in exports.get_exported_processes():
            ptid = process.ptid
            if ptid is None:
                raise ValueError("process class {} has undefined ptid."
                                 .format(process))
            if ptid in self.process_types:
                warnings.repeated_registration('process', ptid)
            self.process_types[ptid] = process

        target_functions_to_register = exports.get_exported_target_functions()
        for target_type in Object.keys(target_functions_to_register):
            if target_type in self.target_type_to_find_function:
                warnings.repeated_registration("target", target_type)
            self.target_type_to_find_function[target_type] = target_functions_to_register[target_type]
        return self

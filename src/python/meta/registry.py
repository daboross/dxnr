from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Tuple

from constants import RoleId, SpawnIdeaKey, SpawnPriorityId, TargetTypeId, TaskId
from constants.tasks import empire_task, room_task
from defs import *
from meta.tasks import Schedule
from utilities import warnings

if TYPE_CHECKING:
    from .registry_exports import Exports


class Database:
    def __init__(self) -> None:
        self.target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self.role_type_to_run_function = {}  # type: Dict[RoleId, Callable[[Room, Creep], None]]
        self.ordered_spawn_possibilities = []  # type: List[Tuple[SpawnPriorityId, Callable[[Room], Optional[Dict[SpawnIdeaKey, int]]]]]
        self.empire_tasks = []  # type: List[Tuple[TaskId, Schedule, Callable[..., None]]]
        self.room_tasks = []  # type: List[Tuple[TaskId, Schedule, Callable[..., None]]]

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
        for task_type_id, task_id, schedule, callback in exports.get_exported_tasks():
            if task_type_id is empire_task:
                self.empire_tasks.append((task_id, schedule, callback))
            elif task_type_id is room_task:
                self.room_tasks.append((task_id, schedule, callback))
            else:
                warnings.unknown_type("task", task_type_id)
        return self

    def finalize(self) -> None:
        self.ordered_spawn_possibilities = _.sortBy(
            _.shuffle(self.ordered_spawn_possibilities),
            lambda t: t[0]
        )

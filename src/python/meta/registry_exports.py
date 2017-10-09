from typing import Callable, Dict, List, Optional, Tuple

from constants import RoleId, SpawnIdeaKey, SpawnPriorityId, TargetTypeId, TaskId
from defs import *
from meta.tasks import Schedule, TaskTypeId
from utilities import warnings


class Exports:
    def __init__(self) -> None:
        self._target_type_to_find_function = {}  # type: Dict[TargetTypeId, Callable[[Creep], Optional[str]]]
        self._role_type_to_run_function = {}  # type: Dict[RoleId, Callable[[Room, Creep], None]]
        self._spawn_needs = []  # type: List[Tuple[SpawnPriorityId, Callable[[Room], Optional[Dict[SpawnIdeaKey, int]]]]]
        self._tasks = []  # type: List[Tuple[TaskTypeId, TaskId, Schedule, Callable[..., None]]]

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

    def spawning_need(self,
                      spawn_priority: SpawnPriorityId,
                      callback: Callable[[Room], Optional[Dict[SpawnIdeaKey, int]]]) -> 'Exports':
        self._spawn_needs.append((spawn_priority, callback))
        return self

    def task(self,
             task_type_id: TaskTypeId,
             task_id: TaskId,
             schedule: Schedule,
             task: Callable[..., None]) -> 'Exports':
        self._tasks.append((task_type_id, task_id, schedule, task))
        return self

    def get_exported_target_functions(self) -> Dict[TargetTypeId, Callable[[Creep], Optional[str]]]:
        return self._target_type_to_find_function

    def get_exported_role_functions(self) -> Dict[RoleId, Callable[[Room, Creep], None]]:
        return self._role_type_to_run_function

    def get_exported_spawn_needs(self) \
            -> List[Tuple[SpawnPriorityId, Callable[[Room], Optional[Dict[SpawnIdeaKey, int]]]]]:
        return self._spawn_needs

    def get_exported_tasks(self) \
            -> List[Tuple[TaskTypeId, TaskId, Schedule, Callable[..., None]]]:
        return self._tasks

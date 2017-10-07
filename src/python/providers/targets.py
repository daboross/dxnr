from typing import Dict, List, Optional, Union, cast

from constants.memkeys import key_memory_targets
from defs import *
from providers import registry
from utilities import warnings

_key_targets_creep_to_targets = 'c'
_key_targets_target_to_creeps = 't'

_mem = None  # type: _Memory
_creep_to_targets = None  # type: Dict[str, Dict[int, str]]
_target_to_creeps = None  # type: Dict[int, Dict[str, List[str]]]


def instantiate() -> None:
    global _mem, _creep_to_targets, _target_to_creeps
    _mem = Memory[key_memory_targets]
    if not _mem:
        _mem = Memory[key_memory_targets] = cast(_Memory, {})
    _creep_to_targets = _mem[_key_targets_creep_to_targets]
    if not _creep_to_targets:
        _creep_to_targets = _mem[_key_targets_creep_to_targets] = {}
    _target_to_creeps = _mem[_key_targets_target_to_creeps] = {}
    if not _target_to_creeps:
        _target_to_creeps = _mem[_key_targets_target_to_creeps] = {}


def _get_object_from_id(object_id: str) -> Optional[RoomObject]:
    object_instance = Game.getObjectById(object_id)
    if object_instance:
        return object_instance
    else:
        return None


def _register_target(creep_name: str, target_type: int, target_id: str) -> None:
    this_creep_targets = _creep_to_targets[creep_name]
    if not this_creep_targets:
        this_creep_targets = _creep_to_targets[creep_name] = {}
    existing_target_id = this_creep_targets[target_type]
    if existing_target_id:
        _unregister_target(creep_name, target_type, existing_target_id)

    this_creep_targets[target_type] = target_id

    this_target_type_creeps = _target_to_creeps[target_type]
    if not this_target_type_creeps:
        this_target_type_creeps = _target_to_creeps[target_type] = {}
    this_target_creeps = this_target_type_creeps[target_id]
    if this_target_creeps:
        this_target_creeps.append(creep_name)
    else:
        this_target_type_creeps[target_id] = [creep_name]


def _unregister_target(creep_name: str, target_type: int, target_id: str) -> None:
    this_creep_targets = _creep_to_targets[creep_name]
    if not this_creep_targets or target_type not in this_creep_targets:
        warnings.unregistering_unregistered_creep(creep_name, target_type)
        return

    del this_creep_targets[target_type]
    if _.isEmpty(this_creep_targets):
        del _creep_to_targets[creep_name]

    this_target_type_creeps = _target_to_creeps[target_type]
    if not this_target_type_creeps or target_type not in this_target_type_creeps:
        warnings.unregistering_unregistered_creep(creep_name, target_type)

    this_target_type_creeps[target_id].remove(creep_name)
    if _.isEmpty(this_target_type_creeps[target_id]):
        del this_target_type_creeps[target_id]


def _find_target(creep: Creep, target_type: int) -> Optional[str]:
    find_functions = registry.get().target_type_to_find_function
    if target_type in find_functions:
        return find_functions[target_type](creep)
    else:
        warnings.missing_registration("target", target_type)
        return None


def get_number_of_targeters(target_type: int, target_id: str) -> int:
    this_target_type_map = _target_to_creeps[target_type]
    if this_target_type_map:
        return _.size(this_target_type_map[target_id])
    else:
        return 0


def get_target(creep: Union[Creep, str], target_type: int) -> Optional[RoomObject]:
    if isinstance(creep, Creep):
        creep_name = creep.name
    else:
        creep_name = cast(str, creep)

    creep_targets = _creep_to_targets[creep_name]
    if not creep_targets:
        return None

    target_id = creep_targets[target_type]

    target = _get_object_from_id(target_id)
    if target:
        return target
    else:
        _unregister_target(creep_name, target_type, target_id)
        return None


def get_or_find_target(creep: Creep, target_type: int) -> Optional[RoomObject]:
    creep_name = creep.name

    existing_target = get_target(creep_name, target_type)
    if existing_target:
        return existing_target

    new_target_id = _find_target(creep, target_type)
    _register_target(creep_name, target_type, new_target_id)
    return _get_object_from_id(new_target_id)

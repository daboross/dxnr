from typing import Any, Dict, Optional

from constants import SecondLevelMemoryKey, TopLevelMemoryId, memkeys
from defs import *

_memory = None  # type: Optional[_Memory]


def instantiate() -> None:
    global _memory, _meta
    _memory = Memory


def top_level_mem_ro(_id: TopLevelMemoryId) -> Dict[str, Dict[SecondLevelMemoryKey, Any]]:
    if _id in _memory:
        return _memory[_id]
    else:
        return {}


def top_level_mem(_id: TopLevelMemoryId) -> Dict[str, Dict[SecondLevelMemoryKey, Any]]:
    if _id in _memory:
        return _memory[_id]
    else:
        mem = {}  # type: Dict[str, Dict[SecondLevelMemoryKey, Any]]
        _memory[_id] = mem
        return mem


def creep_mem_ro(creep_name: str) -> Dict[SecondLevelMemoryKey, Any]:
    creeps = top_level_mem_ro(memkeys.key_memory_creeps)
    if creep_name in creeps:
        return creeps[creep_name]
    else:
        return {}


def creep_mem(creep_name: str) -> Dict[SecondLevelMemoryKey, Any]:
    creeps = top_level_mem(memkeys.key_memory_creeps)
    if creep_name in creeps:
        return creeps[creep_name]
    else:
        mem = {}  # type: Dict[SecondLevelMemoryKey, Any]
        creeps[creep_name] = mem
        return mem

from typing import Any, Dict, Optional

from constants import SecondLevelMemoryKey, TopLevelMemoryId
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


def top_level_mem(_id: TopLevelMemoryId) -> Dict[SecondLevelMemoryKey, Any]:
    if _id in _memory:
        return _memory[_id]
    else:
        mem = {}  # type: Dict[SecondLevelMemoryKey, Any]
        _memory[_id] = mem
        return mem

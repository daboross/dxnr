from typing import Dict, List, Optional

from defs import *

_spawns_per_room = None  # type: Optional[Dict[str, List[StructureSpawn]]]


def instantiate() -> None:
    global _spawns_per_room
    _spawns_per_room = {}
    for spawn_name in Object.keys(Game.spawns):
        spawn = Game.spawns[spawn_name]
        room_name = spawn.pos.roomName
        if room_name in _spawns_per_room:
            _spawns_per_room[room_name].append(spawn)
        else:
            _spawns_per_room[room_name] = [spawn]


def spawns_in(room_name: str) -> List[StructureSpawn]:
    return _spawns_per_room[room_name] or []

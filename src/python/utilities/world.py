from typing import List, Tuple, cast

from defs import *

room_regex = __new__(RegExp("^(W|E)([0-9]{1,3})(N|S)([0-9]{1,3})$"))


def parse_room_to_xy(room_name):
    # type: (str) -> Tuple[int, int]
    matches = room_regex.exec(room_name)
    if not matches:
        return 0, 0
    if matches[1] == "W":
        x = -int(matches[2]) - 1
    else:
        x = +int(matches[2])
    if matches[3] == "N":
        y = -int(matches[4]) - 1
    else:
        y = +int(matches[4])
    return x, y


def distance(pos1: RoomPosition, pos2: RoomPosition) -> int:
    if pos1.roomName == pos2.roomName:
        return max(abs(pos1.x - pos2.x), abs(pos1.y - pos2.y))
    room_1_pos = parse_room_to_xy(pos1.roomName)
    room_2_pos = parse_room_to_xy(pos2.roomName)
    world_pos_1_x = room_1_pos[0] * 49 + pos1.x
    world_pos_1_y = room_1_pos[1] * 49 + pos1.y
    world_pos_2_x = room_2_pos[0] * 49 + pos2.x
    world_pos_2_y = room_2_pos[1] * 49 + pos2.y
    return max(abs(world_pos_1_x - world_pos_2_x), abs(world_pos_1_y - world_pos_2_y))


def pos_xy_to_int(pos: RoomPosition) -> int:
    return pos.x | pos.y << 6


def int_xy_to_pos(xy: int, room_name: str) -> RoomPosition:
    return __new__(RoomPosition(xy & 0x3F, xy >> 6 & 0x3F, room_name))


def xy_to_int(x: int, y: int) -> int:
    return x | y << 6


def int_to_xy(xy: int) -> Tuple[int, int]:
    return xy & 0x3F, xy >> 6 & 0x3F


def is_position_structure_free(room: Room, x: int, y: int) -> bool:
    if Game.map.getTerrainAt(x, y, room.name) == 'wall':
        return False
    for structure in cast(List[Structure], room.lookForAt(LOOK_STRUCTURES, x, y)):
        if not is_structure_passable(structure):
            return False
    for site in cast(List[ConstructionSite], room.lookForAt(LOOK_CONSTRUCTION_SITES, x, y)):
        if not is_construction_site_passable(site):
            return False

    return True


def is_structure_passable(structure: Structure) -> bool:
    if structure.structureType == STRUCTURE_RAMPART and cast(StructureRampart, structure).my:
        return True
    if structure.structureType == STRUCTURE_CONTAINER:
        return True
    if structure.structureType == STRUCTURE_ROAD:
        return True
    return False


def is_construction_site_passable(site: ConstructionSite) -> bool:
    if not site.my:
        return False

    return (
        site.structureType == STRUCTURE_RAMPART
        or site.structureType == STRUCTURE_CONTAINER
        or site.structureType == STRUCTURE_ROAD
    )

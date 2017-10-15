from typing import Any, Dict, List, NewType, Optional, Tuple, cast

from defs import *
from utilities import warnings, world

MoveReason = NewType("MoveReason", int)

reason_moving_to_target = MoveReason(1)
reason_moving_out_of_way = MoveReason(2)

IDLE_ABOUT = 6
MOVE_THEN_WORK = 5
CONSTANT_MOVEMENT = 4
SEMICONSTANT_MOVEMENT = 3
MILITARY = 2
MOVE_THEN_STOP = 1

dir_to_dx_dy = {
    TOP_LEFT: [-1, -1],
    LEFT: [-1, 0],
    BOTTOM_LEFT: [-1, 1],
    TOP: [0, -1],
    BOTTOM: [0, 1],
    TOP_RIGHT: [1, -1],
    RIGHT: [1, 0],
    BOTTOM_RIGHT: [1, 1],
}


def dxdy_to_direction(dx: int, dy: int) -> int:
    """
    Gets the screeps direction constant from a given dx and dy.

    Returns -1 for invalid dx/dy.
    """
    direction = None
    if dx < 0:
        if dy < 0:
            direction = TOP_LEFT
        elif dy == 0:
            direction = LEFT
        elif dy > 0:
            direction = BOTTOM_LEFT
    elif dx == 0:
        if dy < 0:
            direction = TOP
        elif dy > 0:
            direction = BOTTOM
    elif dx > 0:
        if dy < 0:
            direction = TOP_RIGHT
        elif dy == 0:
            direction = RIGHT
        elif dy > 0:
            direction = BOTTOM_RIGHT
    if direction is None:
        warnings.warn("dx/dy passed to dxdy_to_direction not known: ({}, {})", dx, dy)
        return -1
    else:
        return direction


_moved_from_per_room = {'-': None}  # type: Dict[str, Optional[Map[int, Tuple[int, MoveReason]]]]
_moved_to_per_room = {'-': None}  # type: Dict[str, Optional[Map[int, Tuple[int, MoveReason]]]]


def instantiate() -> None:
    global _moved_from_per_room, _moved_to_per_room
    _moved_from_per_room = {'-': None}
    _moved_to_per_room = {'-': None}


def initialize_moved_maps_for(room_name: str) -> None:
    if room_name not in _moved_to_per_room:
        _moved_to_per_room[room_name] = __new__(Map())
    if room_name not in _moved_from_per_room:
        _moved_from_per_room[room_name] = __new__(Map())


def set_moved_in(room: str, xy: int, new_xy: int, reason: MoveReason) -> None:
    places_moved_from_here = _moved_from_per_room[room]
    places_moved_to_here = _moved_to_per_room[room]

    if places_moved_from_here and places_moved_from_here.has(xy):
        old_target, old_reason = places_moved_from_here.get(xy)
        old_target_from = places_moved_to_here.get(old_target)
        if old_target_from == xy:
            places_moved_to_here.delete(old_target)

    places_moved_from_here.set(xy, (new_xy, reason))
    places_moved_to_here.set(new_xy, (xy, reason))


def undo_moved_in(room: str, xy: int, new_xy: int) -> None:
    _moved_from_per_room[room].delete(xy)
    new_xy_to_move = _moved_to_per_room[room]
    if new_xy_to_move.has(new_xy):
        orig_xy, _reason = new_xy_to_move.get(new_xy)
        if orig_xy == xy:
            new_xy_to_move.delete(new_xy)


def transform_to_direction(orig_xy: int, new_xy: int) -> int:
    orig_x, orig_y = world.int_to_xy(orig_xy)
    new_x, new_y = world.int_to_xy(new_xy)

    return dxdy_to_direction(new_x - orig_x, new_y - orig_y)


RedirectResult = NewType("RedirectResult", bool)
redirect_success = RedirectResult(True)
redirect_failure = RedirectResult(False)


def find_and_set_redirect(creep: Creep, now_open_xy: int, taken_new_xy: int) -> RedirectResult:
    """
    Fairly recursive method to try and find good places to put creeps that are in the way.

    Or at least, that's the intent. Right now it'll just find a place that's open if it can, and return otherwise.

    Eventually, this method should:
    - Look around at places that are open, or with creeps that haven't moved
    - Poll the role class for the given creep to see if any of these places are OK
    - If all the open spaces are bad, but some of the taken but not-moved creeps are ok, repeat this process
      for each of those creeps to see if we can find a place
    """
    possibilities = []
    creep_x = creep.pos.x
    creep_y = creep.pos.y

    places_moved_to_here = _moved_to_per_room[creep.pos.roomName]
    places_moved_from_here = _moved_from_per_room[creep.pos.roomName]

    for x in range(max(1, creep_x - 1), min(49, creep_x + 2)):
        for y in range(max(1, creep_y - 1), min(49, creep_y + 2)):
            if x == creep_x and y == creep_y:
                continue
            if not world.is_position_structure_free(creep.room, x, y):
                continue

            pos_xy = world.xy_to_int(x, y)

            if pos_xy == taken_new_xy:
                continue

            creep_here = creep.room.lookForAt(LOOK_CREEPS, x, y)[0]
            if creep_here and ((not places_moved_from_here.has(pos_xy))
                               and not pos_xy == now_open_xy):
                continue  # this should change

            if places_moved_to_here.has(pos_xy):
                continue  # this should change - maybe?
            possibilities.append(pos_xy)

    if len(possibilities):
        xy = _.sample(possibilities)
        x, y = world.int_to_xy(xy)
        direction = dxdy_to_direction(x - creep_x, y - creep_y)
        if direction >= 0:
            cast(Any, creep).__real_move(direction)
            set_moved_in(creep.pos.roomName, world.xy_to_int(creep_x, creep_y), xy, reason_moving_out_of_way)
            return redirect_success
    return redirect_failure


def new_move(direction: int) -> int:
    self = cast(Creep, this)
    room_name = self.pos.roomName

    current_xy = world.xy_to_int(self.pos.x, self.pos.y)

    initialize_moved_maps_for(room_name)

    original_redirect = _moved_from_per_room[room_name].get(current_xy)

    internal_result = this.__real_move(direction)
    if internal_result != OK:
        return internal_result

    diff = dir_to_dx_dy[direction]
    if diff == undefined:
        # TODO: warning here?
        return internal_result

    new_x = self.pos.x + diff[0]
    new_y = self.pos.y + diff[1]

    new_xy = world.xy_to_int(new_x, new_y)

    if new_x > 49 or new_x < 0 or new_y > 49 or new_y < 0:
        if internal_result == OK:
            set_moved_in(self.pos.roomName, current_xy, new_xy, reason_moving_to_target)
        return internal_result

    creep_here = cast(List[Creep], self.room.lookForAt(LOOK_CREEPS, new_x, new_y))[0]
    places_moved_to_here = _moved_to_per_room[self.pos.roomName]
    places_moved_from_here = _moved_from_per_room[self.pos.roomName]

    still_moving = True
    redirect_creep = None
    if creep_here:
        if creep_here.my:
            if not places_moved_from_here or not places_moved_from_here.has(new_xy):
                # the creep hasn't moved yet
                redirect_creep = creep_here
        else:
            still_moving = False

    if still_moving and places_moved_to_here and places_moved_to_here.has(new_xy):
        moving_from, move_reason = places_moved_to_here.get(new_xy)
        if move_reason is reason_moving_out_of_way:
            other_x, other_y = world.int_to_xy(moving_from)
            if redirect_creep is None:
                redirect_creep = cast(List[Creep], self.room.lookForAt(LOOK_CREEPS, other_x, other_y))[0]
            else:
                # this scenario is not expected, but it's best to handle it gracefully.
                warnings.warn("creep wrongly registered for moving to ({},{}) from ({},{}) "
                              "(creep at location was not registered to move away)",
                              new_x, new_y, other_x, other_y)
                still_moving = False
        else:
            still_moving = False

    if redirect_creep:
        redirect_result = find_and_set_redirect(redirect_creep, current_xy, new_xy)
        if redirect_result is redirect_failure:
            still_moving = False

    if still_moving:
        set_moved_in(self.pos.roomName, current_xy, new_xy, reason_moving_to_target)
        return internal_result
    else:
        if original_redirect:
            this.__real_move(transform_to_direction(current_xy, original_redirect[0]))
        else:
            self.cancelOrder('move')
        return ERR_NO_PATH  # TODO: determine best error code here


def apply_prototypes() -> None:
    if not _.isFunction(Creep.prototype.__real_move):
        Creep.prototype.__real_move = Creep.prototype.move
    Creep.prototype.move = new_move


def get_current_movements_per_room() -> Dict[str, Optional[Map[int, Tuple[int, MoveReason]]]]:
    return _moved_from_per_room

from constants.tasks import empire_task, task_visualize_movement
from defs import *
from meta.registry_exports import Exports
from meta.tasks import Schedule
from providers.movement import passing_movement
from utilities import visuals, world

COLOR_WINE = "#6d213c"
COLOR_RAW_UMBER = "#946846"
COLOR_DARK_KHAKI = "#baab68"
COLOR_STRAW = "#e3c16f"
COLOR_MELLOW_YELLOW = "#faff70"


def draw_arrow(room_name: str,
               origin_x: int,
               origin_y: int,
               destination_x: int,
               destination_y: int,
               color: str,
               width: float) -> None:
    end_x = origin_x + (destination_x - origin_x) * 0.95
    end_y = origin_y + (destination_y - origin_y) * 0.95

    visuals.draw_line(room_name, origin_x, origin_y, end_x, end_y, {
        'opacity': 0.45,
        'fill': color,
        'width': width,
    })

    circle_x = origin_x + (destination_x - origin_x) * 0.9
    circle_y = origin_y + (destination_y - origin_y) * 0.9
    visuals.draw_circle(room_name, circle_x, circle_y, {
        'opacity': 0.45,
        'fill': color,
        'radius': width * 1.5
    })


def visualize_passing_movement() -> None:
    data = passing_movement.get_current_movements_per_room()
    for room_name in Object.keys(data):
        room_data = data[room_name]
        if room_data is None:
            continue
        for origin_xy, (destination_xy, move_reason) in list(room_data.entries()):
            origin_x, origin_y = world.int_to_xy(origin_xy)
            destination_x, destination_y = world.int_to_xy(destination_xy)
            draw_arrow(room_name, origin_x, origin_y, destination_x, destination_y, COLOR_STRAW, 0.1)


exports = Exports().task(empire_task, task_visualize_movement, Schedule.always(), visualize_passing_movement)

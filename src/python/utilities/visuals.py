"""
A copy of the Screeps RoomVisual class, allowing direct access without creating RoomVisual classes.

Copied from https://github.com/screeps/engine/blob/36e76eacb7d8295a2767ad75a5d859153928301b/src/game/rooms.js#L1054.
"""
from typing import Any, List, Tuple, Union

from defs import *


def draw_circle(room_name: str, x: Union[int, float], y: Union[int, float], style: Any = undefined) -> None:
    """
    Draw a line
    :param room_name: The room name
    :param x: The center X coordinate
    :param y: The center Y coordinate
    :param style: An object with the following properties:
    radius: Circle radius, default is 0.15
    fill: The color in any web format, default is #ffffff
    opacity: Opacity value, default is 0.5
    stroke: Stroke color in any web format, default is undefined
    strokeWidth: stroke line width, default is 0.1
    lineStyle: either undefined (solid line), dashed, or dotted. Default is undefined
    """
    console.addVisual(room_name, {
        't': 'c',
        'x': x,
        'y': y,
        's': style,
    })


def draw_line(room_name: str, x1: Union[int, float], y1: Union[int, float], x2: Union[int, float],
              y2: Union[int, float], style: Any = undefined) -> None:
    """
    Draw a line.
    :param room_name: The room name
    :param x1: The start X coordinate
    :param y1: The start Y coordinate
    :param x2: The end X coordinate
    :param y2: The end Y coordinate
    :param style: An object with the following properties:
    width: Line width, default is 0.1
    color: Line color in any web format, default is #ffffff
    opacity: Opacity value, default is 0.5
    lineStyle: Either undefined (solid line), dashed, or dotted. Default is undefined
    """
    console.addVisual(room_name, {
        't': 'l',
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        's': style,
    })


def draw_rect(room_name: str, x: Union[int, float], y: Union[int, float], w: Union[int, float], h: Union[int, float],
              style: Any = undefined) -> None:
    """
    Draw a rectangle.
    :param room_name: The room name
    :param x: The X coordinate of the top-left corner
    :param y: The Y coordinate of the top-left corner
    :param w: The width of the rectangle
    :param h: The height of the rectangle
    :param style: An object with the following properties:
    fill: The color in any web format, default is #ffffff
    opacity: Opacity value, default is 0.5
    stroke: Stroke color in any web format, default is undefined
    strokeWidth: stroke line width, default is 0.1
    lineStyle: either undefined (solid line), dashed, or dotted. Default is undefined
    """
    console.addVisual(room_name, {
        't': 'r',
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        's': style,
    })


def draw_poly(room_name: str, points: List[Union[List[int], Tuple[int, int]]], style: Any = undefined) -> None:
    """
    Draw a polyline.
    :param room_name: The room name
    :param points: A list of points, each a tuple of 2 numbers (10, 15)
    :param style: An object with the following properties:
    fill: The color in any web format, default is #ffffff
    opacity: Opacity value, default is 0.5
    stroke: Stroke color in any web format, default is undefined
    strokeWidth: stroke line width, default is 0.1
    lineStyle: either undefined (solid line), dashed, or dotted. Default is undefined
    """
    console.addVisual(room_name, {
        't': 'p',
        'points': points,
        's': style,
    })


def draw_text(room_name: str, x: Union[int, float], y: Union[int, float], message: str, style: Any = undefined) -> None:
    """
    Draw a text label.
    :param room_name: The room name
    :param x: The X coordinate of the label baseline point
    :param y: The Y coordinate of the label baseline point
    :param message: The text message
    :param style: An object with the following properties:
    color: Font color in any web format, default is #ffffff
    size: Font size, default is 0.5
    align: Text align, either center, left, or right, default is center
    opacity: Opacity value, default is 1.0
    """
    console.addVisual(room_name, {
        't': 't',
        'text': message,
        'x': x,
        'y': y,
        's': style,
    })


def get_size(room_name: str) -> int:
    return console.getVisualSize(room_name)


def clear(room_name: str) -> None:
    return console.clearVisual(room_name)

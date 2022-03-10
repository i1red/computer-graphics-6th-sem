from typing import Callable, Any
from entities import Line, Rectangle, Point


def divide_rectangle_left(rectangle: Rectangle, x: float) -> Rectangle:
    p1 = rectangle.point1
    p2 = Point(x, rectangle.point2.y)
    return Rectangle(p1, p2)


def divide_rectangle_right(rectangle: Rectangle, x: float) -> Rectangle:
    p1 = Point(x, rectangle.point1.y)
    p2 = rectangle.point2
    return Rectangle(p1, p2)


def divide_rectangle_lower(rectangle: Rectangle, y: float) -> Rectangle:
    p1 = rectangle.point1
    p2 = Point(rectangle.point2.x, y)
    return Rectangle(p1, p2)


def divide_rectangle_higher(rectangle: Rectangle, y: float) -> Rectangle:
    p1 = Point(rectangle.point1.x, y)
    p2 = rectangle.point2
    return Rectangle(p1, p2)


def get_rectangle_from_points(points: list[Point]) -> Rectangle:
    p1 = Point(0, 0)
    max_x = 0
    max_y = 0
    for p in points:
        if p.x > max_x:
            max_x = p.x
        if p.y > max_y:
            max_y = p.y
    p2 = Point(max_x + 1, max_y + 1)
    return Rectangle(p1, p2)


def get_node_points_vertical(point: Point, points: list[Point]) -> tuple[list[Point], list[Point]]:
    node_points_left = []
    node_points_right = []
    for p in points:
        if p.x < point.x:
            node_points_left.append(p)
        if (p.x >= point.x) & (point.y != p.y):
            node_points_right.append(p)
    return node_points_left, node_points_right


def get_node_points_horizontal(point: Point, points: list[Point]) -> tuple[list[Point], list[Point]]:
    node_points_left = []
    node_points_right = []
    for p in points:
        if p.y < point.y:
            node_points_left.append(p)
        if (p.y >= point.y) & (point.x != p.x):
            node_points_right.append(p)
    return node_points_left, node_points_right


def get_middle_point(points: list[Point], key: Callable[[Point], Any]) -> Point:
    ret = sorted(points, key=key)
    middle = len(points) // 2
    return ret[middle]


def get_line_segment(line: Line, rectangle: Rectangle) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((rectangle.point1.x, rectangle.point2.x), (line.y, line.y)) if line.x is None \
        else ((line.x, line.x), (rectangle.point1.y, rectangle.point2.y))


def rectangle_crosses_region(rectangle: Rectangle, region: Rectangle) -> bool:
    return not (rectangle.point2.x < region.point1.x or rectangle.point1.x > region.point2.x
                or rectangle.point2.y < region.point1.y or rectangle.point1.y > region.point2.y)


def point_is_in_rectangle(point: Point, rectangle: Rectangle) -> bool:
    return rectangle.point1.x <= point.x <= rectangle.point2.x and rectangle.point1.y <= point.y <= rectangle.point2.y

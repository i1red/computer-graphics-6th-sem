from typing import List, Set

from point import Point
from utils import get_position, calc_distance


def quick_hull(points) -> Set[Point]:
    if len(points) < 3:
        return set(points)

    min_x, max_x = min(points, key=lambda point: point.x), max(points, key=lambda point: point.x)

    hull = set()

    _quick_hull_impl([p for p in points if get_position(min_x, max_x, p) == -1], min_x, max_x, hull)
    _quick_hull_impl([p for p in points if get_position(min_x, max_x, p) == 1], min_x, max_x, hull)

    return hull


def _quick_hull_impl(points: List[Point], p1: Point, p2: Point, hull: Set[Point]) -> None:
    try:
        farthest_point = max(points, key=lambda point: calc_distance(p1, p2, point))

        side1, side2 = -1 * get_position(farthest_point, p1, p2), -1 * get_position(farthest_point, p2, p1)
        _quick_hull_impl([p for p in points if get_position(farthest_point, p1, p) == side1], farthest_point, p1, hull)
        _quick_hull_impl([p for p in points if get_position(farthest_point, p2, p) == side2], farthest_point, p2, hull)
    except ValueError:
        hull.update({p1, p2})

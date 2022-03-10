from typing import List

from point import Point
from utils import get_side


def jarvis_hull(points: List[Point]) -> List[Point]:
    if len(points) <= 3:
        return list(points)

    points = list(points)  # copy list

    leftmost_index = get_leftmost_point_index(points)
    leftmost_point = points[leftmost_index]
    points[leftmost_index], points[-1] = points[-1], points[leftmost_index]

    result = [leftmost_point]

    index = find_next_index(points, leftmost_point)
    point = points[index]
    points.pop(index)

    while point != leftmost_point:
        result.append(point)
        index = find_next_index(points, point)
        point = points[index]
        points.pop(index)

    return result


def get_leftmost_point_index(points: List[Point]) -> int:
    return min(range(len(points)), key=lambda i: (points[i].x, points[i].y))


def find_next_index(points: List[Point], point: Point) -> int:
    next_, index = points[0], 0

    for i in range(len(points)):
        if get_side(points[i], next_, point) == -1:
            next_, index = points[i], i

    return index

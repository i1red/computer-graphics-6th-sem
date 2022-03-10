import math

from typing import List

from point import Point
from utils import get_side


def graham_hull(points: List[Point]) -> List[Point]:
    if len(points) <= 3:
        return list(points)

    points = list(points)  # copy list

    ind = get_lowest_point_index(points)
    points[ind], points[0] = points[0], points[ind]

    points = sorted(points, key=lambda point: math.atan2(point.y - points[0].y, point.x - points[0].x))
    hull = points[:3]

    for point in points[3:]:
        while len(hull) >= 2 and get_side(point, hull[-2], hull[-1]) <= 0:
            hull.pop(-1)

        hull.append(point)

    return hull


def get_lowest_point_index(points: List[Point]) -> int:
    return min(range(len(points)), key=lambda i: (points[i].y, points[i].x))


from typing import Tuple, Optional, List
import math

from data_types import Point, Arc


def get_circle(a: Point, b: Point, c: Point) -> Tuple[Optional[float], Optional[Point]]:
    # check if bc is a "right turn" from ab
    if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0:
        return None, None

    A, B, C, D = b.x - a.x, b.y - a.y, c.x - a.x, c.y - a.y

    E = A * (a.x + b.x) + B * (a.y + b.y)
    F = C * (a.x + c.x) + D * (a.y + c.y)
    G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

    # Points are co-linear
    if G == 0:
        return None, None

    center_x, center_y = (D * E - B * F) / G, (A * F - C * E) / G

    radius = math.sqrt((a.x - center_x) ** 2 + (a.y - center_y) ** 2)
    max_x = center_x + radius
    center = Point(center_x, center_y)

    return max_x, center


def get_intersection(p0: Point, p1: Point, l: float) -> Point:
    # get the intersection of two parabolas
    p = p0
    if p0.x == p1.x:
        py = (p0.y + p1.y) / 2
    elif p1.x == l:
        py = p1.y
    elif p0.x == l:
        py = p0.y
        p = p1
    else:
        # use quadratic formula
        z0 = 2 * (p0.x - l)
        z1 = 2 * (p1.x - l)

        a = 1 / z0 - 1 / z1
        b = -2 * (p0.y / z0 - p1.y / z1)
        c = (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1

        py = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

    px = (p.x ** 2 + (p.y - py) ** 2 - l ** 2) / (2 * p.x - 2 * l)
    res = Point(px, py)
    return res


def get_arc_intersection(point: Point, arc: Arc) -> Optional[Point]:
    # check whether a new parabola at point p intersect with arc i
    if arc is None or arc.point.x == point.x:
        return None

    a, b = 0, 0

    if arc.prev is not None:
        a = get_intersection(arc.prev.point, arc.point, point.x).y
    if arc.next is not None:
        b = get_intersection(arc.point, arc.next.point, point.x).y

    if ((arc.prev is None) or (a <= point.y)) and ((arc.next is None) or (point.y <= b)):
        py = point.y
        px = ((arc.point.x) ** 2 + (arc.point.y - py) ** 2 - point.x ** 2) / (2 * arc.point.x - 2 * point.x)
        return Point(px, py)

    return None


def get_bounding_box(points: List[Point]) -> Tuple[float, float, float, float]:
    min_x, max_x, min_y, max_y = 0, 0, 0, 0

    for point in points:
        min_x, max_x = min(point.x, min_x), max(point.x, max_x)
        min_y, max_y = min(point.y, min_y), max(point.y, max_y)

    dx, dy = (max_x - min_x + 1) / 5, (max_y - max_y + 1) / 5
    min_x, max_x = min_x - dx, max_x + dx
    min_y, max_y = min_y - dy, max_y + dy

    return min_x, max_x, min_y, max_y

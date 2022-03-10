import math

from point import Point


def sign(value: float) -> int:
    return int(math.copysign(1, value))


def calc_cross_product(p1: Point, p2: Point, p: Point) -> float:
    return (p.x - p1.x) * (p2.y - p1.y) - (p.y - p1.y) * (p2.x - p1.x)


def calc_distance(p1: Point, p2: Point, p: Point) -> float:
    return abs(calc_cross_product(p1, p2, p))


def get_position(p1: Point, p2: Point, p: Point) -> int:
    if math.atan2(-p1.x, -p1.y) < math.atan2(-p2.x, -p2.y):
        p1, p2 = p2, p1

    return sign(calc_cross_product(p1, p2, p))

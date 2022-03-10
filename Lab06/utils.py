from point import Point


def get_side(a: Point, b: Point, c: Point) -> int:
    rotation = get_rotation(a, b, c)

    if rotation > 0:
        return 1
    if rotation < 0:
        return -1
    return 0


def get_rotation(a: Point, b: Point, c: Point) -> float:
    return (c.y - a.y) * (b.x - a.x) - (b.y - a.y) * (c.x - a.x)

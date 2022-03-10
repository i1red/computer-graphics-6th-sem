import enum
import math

from graph import Point, Edge


class PointLocation(enum.IntEnum):
    Left = 0,
    Right = 1,
    None_ = 2


def get_point_location(point: Point, chain: list[Edge]) -> PointLocation:
    while len(chain) > 0:
        mid = len(chain) // 2
        e = chain[mid]

        if e.start.y <= point.y <= e.end.y:
            if math.atan2(point.y - e.start.y, point.x - e.start.x) > e.rotation:
                return PointLocation.Right
            else:
                return PointLocation.Left
        elif point.y < e.start.y:
            chain = chain[:mid]
        else:
            chain = chain[mid + 1:]

    return PointLocation.None_


def find(point: Point, chains: list[list[Edge]]):
    left_chain, right_chain = None, None

    while len(chains) > 0:
        mid = len(chains) // 2
        mid_chain = chains[mid]
        point_location = get_point_location(point, mid_chain)

        if point_location == PointLocation.Right:
            right_chain = mid_chain
            chains = chains[:mid]
        elif point_location == PointLocation.Left:
            left_chain = mid_chain
            chains = chains[mid + 1:]
        else:
            break

    return left_chain, right_chain


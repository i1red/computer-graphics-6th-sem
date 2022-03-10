import random

from typing import List

from point import Point
from utils import get_rotation
from jarvis_hull import jarvis_hull
from graham_hull import graham_hull


def divide_and_conquer_hull(points: List[Point]) -> List[Point]:
    if len(points) <= 8:
        return jarvis_hull(points)

    mid = len(points) // 2
    return merge(divide_and_conquer_hull(points[:mid]), divide_and_conquer_hull(points[mid:]))


def merge(left_points: List[Point], right_points: List[Point]) -> List[Point]:
    if left_points[0].x > right_points[0].x:
        left_points, right_points = right_points, left_points

    inner_point = get_triangle_centroid(get_random_triangle(left_points))

    if not is_point_inside_polygon(inner_point, right_points):
        next_left, next_right = find_next_left(inner_point, right_points), find_next_right(inner_point, right_points)

        right_points = remove_chain(next_left, next_right, right_points) \
            if get_rotation(inner_point, next_left, next_right) >= 0 \
            else remove_chain(next_left, next_left, right_points)

    return graham_hull(concatenate(left_points, right_points))


def concatenate(left_points: List[Point], right_points: List[Point]) -> List[Point]:
    return left_points + right_points if left_points[0].x < right_points[0].x else right_points + left_points


def get_random_triangle(points: List[Point]) -> List[Point]:
    triangle = []

    for i in range(3):
        while (point := random.choice(points)) in triangle:
            pass

        triangle.append(point)

    return triangle


def get_triangle_centroid(triangle: List[Point]) -> Point:
    return Point(sum(x for x, _ in triangle) / 3, sum(y for _, y in triangle) / 3)


def is_point_inside_polygon(point: Point, points: List[Point]) -> bool:
    count = 0

    for start, end in zip(points, points[1:] + points[:1]):
        if start.y > end.y:
            end, start = start, end

        if get_rotation(point, start, end) >= 0:
            count += 1

    return count % 2 != 0


def find_next_left(point: Point, points: List[Point]) -> Point:
    next_left = points[0]

    for current_point in points[1:]:
        if get_rotation(current_point, point, next_left) > 0:
            next_left = current_point

    return next_left


def find_next_right(point: Point, points: List[Point]) -> Point:
    next_right = points[0]

    for current_point in points[1:]:
        if get_rotation(current_point, point, next_right) < 0:
            next_right = current_point

    return next_right


def remove_chain(left_point: Point, right_point: Point, hull: List[Point]) -> List[Point]:
    hull, i = list(hull), 0

    while i < len(hull):
        current = hull[i]
        if current != left_point and current != right_point and get_rotation(left_point, current, right_point) > 0:
            hull.pop(i)
        else:
            i += 1

    return hull


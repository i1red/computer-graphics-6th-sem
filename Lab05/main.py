import random
import math

from typing import List, Set, Iterable, Tuple

import matplotlib.pyplot as plt

from point import Point
from quick_hull import quick_hull


def get_coordinates(points: Iterable[Point]) -> Tuple[List[float], List[float]]:
    points_list = sorted(points, key=lambda point: math.atan2(-point.x, -point.y), reverse=True)
    points_list = points_list + points_list[:1]
    return [x for x, _ in points_list], [y for _, y in points_list]


def plot_result(points: List[Point], hull: Set[Point]) -> None:
    plt.figure(figsize=(12, 12))

    plt.plot(*get_coordinates(hull), color='#0000aa')  # edges
    plt.plot([x for x, _ in points], [y for _, y in points], '.', markersize=12, color="#000000")
    plt.plot([x for x, _ in hull], [y for _, y in hull], '.', markersize=25, color="#ff0000")

    plt.show()


def main():
    points = [Point(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(10)]
    hull = quick_hull(points)

    plot_result(points, hull)


if __name__ == '__main__':
    main()

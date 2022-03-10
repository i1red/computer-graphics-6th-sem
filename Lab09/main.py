import random
from typing import List, Final

import matplotlib.pyplot as plt

from voronoi import voronoi
from data_types import Point, Segment


MIN_X: Final = -5
MAX_X: Final = 15
MIN_Y: Final = -5
MAX_Y: Final = 15

PLOT_PADDING: Final = 0.03  # part of (max - min)


def random_point() -> Point:
    return Point(random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_X))


def plot_result(points: List[Point], lines: List[Segment]) -> None:
    plt.figure(figsize=(12, 12))

    x_padding, y_padding = (MAX_X - MIN_X) * PLOT_PADDING, (MAX_Y - MIN_Y) * PLOT_PADDING
    plt.xlim((MIN_X - x_padding, MAX_X + x_padding))
    plt.ylim((MIN_Y - y_padding, MAX_Y + y_padding))

    for line in lines:
        start, end = line.start, line.end
        plt.plot([start.x, end.x], [start.y, end.y], color='#0000aa', linewidth=0.6)

    plt.plot([p.x for p in points], [p.y for p in points], '.', markersize=6, color="#000000")

    plt.show()


def main():
    points = [random_point() for _ in range(40)]
    points = [Point(0, 3), Point(2, 7), Point(4, 5), Point(5, 0), Point(8, 9), Point(9, 2), Point(11, 6)]
    voronoi_s = voronoi(points)
    for s in voronoi_s:
        print(s)
    plot_result(points, voronoi_s)


if __name__ == '__main__':
    main()

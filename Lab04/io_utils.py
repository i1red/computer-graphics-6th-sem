from typing import Optional

import matplotlib.pyplot as plt
from matplotlib import patches

from entities import Point, Node
from utils import get_line_segment


def read_points(filename: str) -> list[Point]:
    with open(filename) as f:
        points = []
        for line in f.readlines():
            coordinates = [float(i) for i in line.split(" ")]
            points.append(Point(coordinates[0], coordinates[1]))

    points.sort()

    for number, p in enumerate(points):
        p.n = number

    return points


def plot_tree(node: Optional[Node]) -> None:
    if node is None:
        return

    line_x, line_y = get_line_segment(node.line, node.rectangle)
    plt.plot(line_x, line_y, color='#000000', linewidth=0.9)

    plot_tree(node.left)
    plot_tree(node.right)


def plot_result(points: list[Point], region_point1: Point, region_point2: Point,
                tree: Node, points_in_region: list[Point]) -> None:
    fig, ax = plt.subplots()
    plot_tree(tree)
    for p in points:
        plt.plot(p.x, p.y, 'o', color='#5050ff', markersize=7)
        plt.text(p.x - 0.3, p.y - 0.4, p.n)

    for p in points_in_region:
        plt.plot(p.x, p.y, 'o', color='#00aa50', markersize=9)

    width = region_point2.x - region_point1.x
    height = region_point2.y - region_point1.y
    rect = patches.Rectangle((region_point1.x, region_point1.y), width, height, linestyle='--', linewidth=1.4, edgecolor='#cc5050',
                             facecolor='none')
    ax.add_patch(rect)

    ax.autoscale()

    plt.show()

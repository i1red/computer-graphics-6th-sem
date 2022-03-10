import math
import itertools

import matplotlib.pyplot as plt

from graph import Edge, Point


_DEFAULT_MAX_GRADATION = 192
_EDGE_MARGIN = 0.15


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def gen_colors(color_num: int, max_gradation: int = _DEFAULT_MAX_GRADATION) -> list[str]:
    colors_per_iteration = 2 ** 3 - 1  # excluding black color
    iterations_num = math.ceil(color_num / colors_per_iteration)
    colors = []

    for i in range(iterations_num):
        gradation = max_gradation - i * (max_gradation // iterations_num)
        colors.extend(list(itertools.product((0, gradation), repeat=3))[1:])

    return [rgb_to_hex(rgb) for rgb in colors[:color_num]]


def show_point_and_chains(point: Point, chains: list[list[Edge]], title: str) -> None:
    plt.figure()
    plt.plot(point.x, point.y, marker='.', markersize=15)
    plt.title(title, fontdict={'size': 16})

    colors = gen_colors(len(chains))
    offset = -len(chains) * _EDGE_MARGIN / 2

    for chain, color in zip(chains, colors):
        for edge in chain:
            plt.plot(
                (edge.start.x + offset, edge.end.x + offset),
                (edge.start.y + offset, edge.end.y + offset),
                color=color
            )
        offset += _EDGE_MARGIN

    plt.show()

from typing import Final

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

from delaunay import delaunay, Triangle, Circle

MIN_X: Final = -200
MAX_X: Final = 200
MIN_Y: Final = -200
MAX_Y: Final = 200

PLOT_PADDING: Final = 0.03  # part of (max - min)


def plot_result(points: np.ndarray, triangles: list[Triangle], circles: list[Circle]):
    plt.figure(figsize=(12, 12))

    x_padding, y_padding = (MAX_X - MIN_X) * PLOT_PADDING, (MAX_Y - MIN_Y) * PLOT_PADDING
    plt.gca().set(xlim=(MIN_X - x_padding, MAX_X + x_padding), ylim=(MIN_Y - y_padding, MAX_Y + y_padding))

    plt.triplot(
        tri.Triangulation([x for x, _ in points], [y for _, y in points], triangles),
        'o-', color='#0000aa', linewidth=0.6
    )

    for circle in circles:
        plt.gcf().gca().add_artist(plt.Circle(*circle, color='#aa2222', fill=False, linewidth=0.5))

    plt.show()


def main() -> None:
    point_count = 7
    points = np.stack(
        (np.random.triangular(MIN_X, (MIN_X + MAX_X) / 2, MAX_X, point_count),
         np.random.triangular(MIN_Y, (MIN_Y + MAX_Y) / 2, MAX_Y, point_count)),
        axis=1
    )
    triangles, circles = delaunay(points)
    plot_result(points, triangles, circles)


if __name__ == '__main__':
    main()

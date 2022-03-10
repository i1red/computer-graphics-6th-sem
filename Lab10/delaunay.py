import random
import math
from typing import Final

import numpy as np

Triangle = tuple[int, int, int]
Circle = tuple[np.ndarray, float]

RADIUS: Final = 1000.


def delaunay(points: np.ndarray, min_x: float = -RADIUS, max_x: float = RADIUS,
             min_y: float = -RADIUS, max_y: float = RADIUS) -> tuple[list[Triangle], list[Circle]]:
    delaunay_algorithm = DelaunayAlgorithm(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
    for point in points:
        delaunay_algorithm.add_point(point)
    return delaunay_algorithm.get_triangles(), delaunay_algorithm.get_circles()


class DelaunayAlgorithm:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float):
        self._coordinates = [np.array([min_x, min_y]), np.array([max_x, min_y]),
                             np.array([max_x, max_y]), np.array([min_x, max_y])]

        # Create two dicts to store triangle neighbours and circumcircles.
        self._triangles = {}
        self._circles = {}

        first_triangle, second_triangle = (0, 1, 3), (2, 3, 1)
        self._triangles[first_triangle] = [second_triangle, None, None]
        self._triangles[second_triangle] = [first_triangle, None, None]

        for triangle in self._triangles:
            self._circles[triangle] = self._get_circumcircle(triangle)

    def _get_circumcircle(self, triangle: Triangle) -> Circle:
        points = np.asarray([self._coordinates[vertex] for vertex in triangle])
        A = np.bmat([
            [2 * (points @ points.T), [[1.], [1.], [1.]]],
            [[[1., 1., 1., 0.]]]
        ])

        b = np.hstack((np.sum(points * points, axis=1), [1.]))
        x = np.linalg.solve(A, b)
        bary_coordinates = x[:-1]
        center = np.dot(bary_coordinates, points)

        radius = np.sum(np.square(points[0] - center))  # squared distance
        return (center, radius)

    def _is_point_in_circumcircle(self, triangle: Triangle, point: np.ndarray) -> bool:
        center, radius = self._circles[triangle]
        return np.sum(np.square(center - point)) <= radius

    def add_point(self, point: np.ndarray) -> None:
        point, index = np.asarray(point), len(self._coordinates)
        self._coordinates.append(point)

        bad_triangles = [triangle for triangle in self._triangles.keys() if self._is_point_in_circumcircle(triangle, point)]

        # Find the CCW boundary (star shape) of the bad triangles,
        # expressed as a list of edges (point pairs) and the opposite
        # triangle to each edge.
        boundary = []
        # Choose a "random" triangle and edge
        triangle = random.choice(bad_triangles)
        edge = 0
        # get the opposite triangle of this edge
        while True:
            opposite_triangle = self._triangles[triangle][edge]
            if opposite_triangle not in bad_triangles:
                boundary.append((triangle[(edge + 1) % 3], triangle[(edge - 1) % 3], opposite_triangle))
                edge = (edge + 1) % 3
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                # Move to next CCW edge in opposite triangle
                edge = (self._triangles[opposite_triangle].index(triangle) + 1) % 3
                triangle = opposite_triangle

        # Remove triangles too near of point p of our solution
        for triangle in bad_triangles:
            del self._triangles[triangle], self._circles[triangle]

        # Retriangle the hole left by bad_triangles
        new_triangles = []
        for e0, e1, opposite_triangle in boundary:
            # Create a new triangle using point p and edge extremes
            triangle = (index, e0, e1)

            # Store circumcenter and circumradius of the triangle
            self._circles[triangle] = self._get_circumcircle(triangle)

            # Set opposite triangle of the edge as neighbour of triangle
            self._triangles[triangle] = [opposite_triangle, None, None]

            # Try to set triangle as neighbour of the opposite triangle
            if opposite_triangle:
                # search the neighbour of opposite_triangle that use edge (e1, e0)
                for i, neighbor in enumerate(self._triangles[opposite_triangle]):
                    if neighbor:
                        if e1 in neighbor and e0 in neighbor:
                            # change link to use our new triangle
                            self._triangles[opposite_triangle][i] = triangle

            # Add triangle to a temporal list
            new_triangles.append(triangle)

        # Link the new triangles each another
        for i, triangle in enumerate(new_triangles):
            self._triangles[triangle][1] = new_triangles[(i + 1) % len(new_triangles)]   # next
            self._triangles[triangle][2] = new_triangles[(i - 1) % len(new_triangles)]   # previous

    def get_triangles(self) -> list[Triangle]:
        return [(a - 4, b - 4, c - 4) for (a, b, c) in self._triangles.keys()
                if a > 3 and b > 3 and c > 3]

    def get_circles(self) -> list[Circle]:
        return [(self._circles[(a, b, c)][0], math.sqrt(self._circles[(a, b, c)][1])) for (a, b, c) in self._triangles
                if a > 3 and b > 3 and c > 3]

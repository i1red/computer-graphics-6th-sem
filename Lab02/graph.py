import json
import math


def get_next_edge(array):
    for edge in array:
        if edge.weight > 0:
            return edge

    return array[0]


def sort_edges(array):
    return sorted(array, key=lambda edge: edge.rotation, reverse=True)


def sum_weights(edges):
    return sum(edge.weight for edge in edges)


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w_in = 0
        self.w_out = 0


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = 0

        self.rotation = math.atan2(end.y - start.y, end.x - start.x)


class Graph:
    def __init__(self, vertices: list[Point], edges: list[Edge]) -> None:
        self.vertices = vertices
        self.edges = edges

    def create_chains(self) -> list[list[Edge]]:
        n = len(self.vertices)
        edges_in = [[] for _ in range(n)]
        edges_out = [[] for _ in range(n)]

        for e in self.edges:
            from_idx, to_idx = self.vertices.index(e.start), self.vertices.index(e.end)

            edges_out[from_idx].append(e)
            edges_in[to_idx].append(e)

            e.weight = 1

        for i in range(1, n - 1):
            self.vertices[i].w_in = sum_weights(edges_in[i])
            self.vertices[i].w_out = sum_weights(edges_out[i])
            edges_out[i] = sort_edges(edges_out[i])
            if self.vertices[i].w_in > self.vertices[i].w_out:
                edges_out[i][0].weight = self.vertices[i].w_in - self.vertices[i].w_out + 1

        for i in range(n - 1, 1, -1):
            self.vertices[i].w_in = sum_weights(edges_in[i])
            self.vertices[i].w_out = sum_weights(edges_out[i])
            edges_in[i] = sort_edges(edges_in[i])
            if self.vertices[i].w_out > self.vertices[i].w_in:
                edges_in[i][0].weight = self.vertices[i].w_out - self.vertices[i].w_in + edges_in[i][0].weight

        num_chains = sum_weights(edges_out[0])
        sorted_edges_out = [sort_edges(v) for v in edges_out]

        return [self._create_chain(sorted_edges_out) for _ in range(num_chains)]

    def _create_chain(self, sorted_edges_out: list[list[Edge]]) -> list[Edge]:
        current_v = 0
        chain = []
        while current_v != len(self.vertices) - 1:
            next_edge = get_next_edge(sorted_edges_out[current_v])
            chain.append(next_edge)
            next_edge.weight -= 1
            current_v = self.vertices.index(next_edge.end)

        return chain

    @classmethod
    def from_json_file(cls, file_name: str) -> 'Graph':
        with open(file_name) as f:
            graph_info = json.load(f)

        vertices = [Point(x, y) for x, y in graph_info['vertices']]
        edges = [Edge(vertices[start_index], vertices[end_index]) for start_index, end_index in graph_info['edges']]

        return cls(vertices, edges)

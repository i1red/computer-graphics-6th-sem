import os

from graph import Graph, Point
from point_location import find
from utils import show_point_and_chains


GRAPH_FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'graph.json')
POINT_COORDINATES = (7.5, 10.5)


def main() -> None:
    graph = Graph.from_json_file(GRAPH_FILE_NAME)

    chains = graph.create_chains()
    point = Point(*POINT_COORDINATES)

    left_chain, right_chain = find(point, chains)
    if left_chain and right_chain:
        title = f'Point is between chains: {chains.index(left_chain)} and {chains.index(right_chain)}'
    else:
        title = f'Point is outside of graph'

    show_point_and_chains(point, chains, title)


if __name__ == '__main__':
    main()

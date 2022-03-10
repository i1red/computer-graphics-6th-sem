from entities import Line, Rectangle, Point, Node

from utils import divide_rectangle_higher, divide_rectangle_lower, divide_rectangle_right, \
    divide_rectangle_left, get_middle_point, get_node_points_horizontal, get_node_points_vertical, \
    get_rectangle_from_points, point_is_in_rectangle, rectangle_crosses_region

from io_utils import read_points, plot_result


def add_children(node: Node, vertical: bool) -> None:
    if len(node.points) <= 1:
        return

    if vertical:
        node_left_points, node_right_points = get_node_points_vertical(node.point, node.points)

        if len(node_left_points) >= 1:
            node_left_point = get_middle_point(node_left_points, lambda p: p.y)
            node.left = Node(node_left_point, divide_rectangle_left(node.rectangle, node.line.x), node_left_points,
                             Line(None, node_left_point.y))
            add_children(node.left, vertical=False)

        if len(node_right_points) >= 1:
            node_right_point = get_middle_point(node_right_points, lambda p: p.y)
            node.right = Node(node_right_point, divide_rectangle_right(node.rectangle, node.line.x), node_right_points,
                              Line(None, node_right_point.y))
            add_children(node.right, vertical=False)
    else:
        node_left_points, node_right_points = get_node_points_horizontal(node.point, node.points)

        if len(node_left_points) >= 1:
            node_left_point = get_middle_point(node_left_points, lambda p: p.x)
            node.left = Node(node_left_point, divide_rectangle_lower(node.rectangle, node.line.y), node_left_points,
                             Line(node_left_point.x, None))
            add_children(node.left, vertical=True)

        if len(node_right_points) >= 1:
            node_right_point = get_middle_point(node_right_points, lambda p: p.x)
            node.right = Node(node_right_point, divide_rectangle_higher(node.rectangle, node.line.y), node_right_points,
                              Line(node_right_point.x, None))
            add_children(node.right, vertical=True)


def build_tree(points: list[Point]) -> Node:
    middle = len(points) // 2
    root = Node(points[middle], get_rectangle_from_points(points), points, Line(points[middle].x, None))
    add_children(root, vertical=True)
    return root


def find_points_in_region(node: Node, region: Rectangle) -> list[Point]:
    points_in_region = []

    if rectangle_crosses_region(node.rectangle, region):
        if point_is_in_rectangle(node.point, region):
            points_in_region.append(node.point)
        if node.left is not None:
            points_in_region.extend(find_points_in_region(node.left, region))
        if node.right is not None:
            points_in_region.extend(find_points_in_region(node.right, region))

    return points_in_region


def main() -> None:
    point1 = Point(2.5, 2.5)
    point2 = Point(8.5, 8.5)

    points = read_points('points.txt')
    tree = build_tree(points)
    plot_result(points, point1, point2, tree, find_points_in_region(tree, Rectangle(point1, point2)))


if __name__ == '__main__':
    main()

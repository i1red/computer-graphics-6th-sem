class Point:
    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)
        self.n = 0

    def __gt__(self, o: 'Point') -> bool:
        if self.x > o.x:
            return True
        elif self.x == o.x and self.y > o.y:
            return True
        else:
            return False

    def __eq__(self, o: 'Point') -> bool:
        if self.x == o.x and self.y == o.y:
            return True
        return False

    def __repr__(self) -> str:
        return str(self.n)


class Rectangle:
    def __init__(self, point1, point2) -> None:
        self.point1 = point1
        self.point2 = point2


class Line:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Node:
    def __init__(self, point, rectangle, points, line) -> None:
        self.point = point
        self.rectangle = rectangle
        self.points = points
        self.line = line
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return str(self.point.n)

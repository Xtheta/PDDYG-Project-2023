class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, low: Point, high: Point):
        self.low = low
        self.high = high

    @property
    def width(self):
        return self.high.x - self.low.x

    @property
    def height(self):
        return self.high.y - self.low.y

    def area(self) -> float:
        return self.width * self.height

    def half_width(self):
        return self.width()/2

    def half_height(self):
        return self.height()/2

    def center(self):
        return Point(self.half_width(), self.half_height())

    def has_point(self, point: Point):
        return self.low.x <= point.x <= self.high.x and self.low.y <= point.y <= self.high.y


class Node:

    def __init__(self, is_leaf, empty,):
        pass

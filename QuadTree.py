import pandas as pd


class Point:

    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = []
        self.data.append(data)

    def __str__(self):
        return "x is " + str(self.x) + " y is " + str(self.y)

    def same_as(self, point: 'Point'):
        return self.x == point.x and self.y == point.y


class Rectangle:
    def __init__(self, low: Point, high: Point):
        self.low = low
        self.high = high

    def __str__(self):
        return " Xmin= " + str(self.low.x) + " Ymin= " \
            + str(self.low.y) + " Xmax= " + str(self.high.x) + " Ymax= " + str(self.high.y)

    @property
    def width(self):
        return self.high.x - self.low.x

    @property
    def height(self):
        return self.high.y - self.low.y

    def area(self):
        return self.width * self.height

    def x_median(self):
        return (self.high.x + self.low.x)/2

    def y_median(self):
        return (self.high.y + self.low.y)/2

    def center(self):
        return Point(self.x_median(), self.y_median())

    def overlaps_point(self, point: Point):
        return self.low.x <= point.x <= self.high.x and self.low.y <= point.y <= self.high.y

    def overlaps(self, rec: 'Rectangle'):
        if self.same_as(rec):
            return True

        rec_xright = max(self.high.x, rec.low.x) == rec.low.x
        if self.high.x == rec.low.x:
            rec_xright = 0

        rec_yright = max(self.high.y, rec.low.y) == rec.low.y
        if self.high.y == rec.low.y:
            rec_yright = 0

        rec_xleft = min(self.low.x, rec.high.x) == rec.high.x
        if self.low.x == rec.high.x:
            rec_xleft = 0

        rec_yleft = min(self.low.y, rec.high.y) == rec.high.y
        if self.low.y == rec.high.y:
            rec_yleft = 0

        return not (rec_xright or rec_xleft or rec_yright or rec_yleft)

    def same_as(self, rec: 'Rectangle'):
        return self.low.x == rec.low.x and self.high.x == rec.high.x and self.low.y == rec.low.y \
            and self.high.y == rec.high.y


class Node:

    def __init__(self, is_leaf, rec: Rectangle, parent: 'Node' = None, point=None):
        self.is_leaf = is_leaf
        self.parent = parent
        self.point = point
        # self.NW, self.NE, self.SW, self.SE = None, None, None, None
        self.directions: list = [None, None, None, None]
        self.rec = rec

    @property
    def is_root(self):
        return self.parent is None

    def isleaf(self) -> bool:
        return self.is_leaf


class QuadTree:

    def __init__(self, rec: Rectangle):
        self.rec = rec
        self.root = Node(True, rec)

    def insert(self, point: Point):
        # if not self.rec.has_point(point):
        #     exit(-1)
        loop_check = 0
        node = self.root
        while loop_check == 0:
            if node.is_leaf:
                if node.point is None:
                    node.point = point
                    loop_check += 1
                else:
                    node = self.split_node(node, node.rec, point)
                    loop_check += 1
            else:
                for child_node in node.directions:
                    if child_node.rec.overlaps_point(point):
                        node = child_node

    def split_node(self, node: Node, rec: Rectangle, point: Point):

        if node.point.same_as(point):
            node.point.data.extend(point.data)
            return node

        node.is_leaf = False

        index = axis(rec, point)

        index2 = axis(rec, node.point)  # mia sinarthsh pou na ta periexei ola

        rectangles = []
        p1 = Point(rec.low.x, rec.center().y)
        p2 = Point(rec.center().x, rec.high.y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(rec.low.x, rec.low.y)
        p2 = Point(rec.center().x, rec.center().y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(rec.center().x, rec.center().y)
        p2 = Point(rec.high.x, rec.high.y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(rec.center().x, rec.low.y)
        p2 = Point(rec.high.x, rec.center().y)
        rectangles.append(Rectangle(p1, p2))

        for i in range(0, 4):
            if i != index and i != index2:
                node.directions[i] = Node(True, rectangles[i], node, None)

        if index != index2:

            node.directions[index] = Node(True, rectangles[index], node, point)
            node.directions[index2] = Node(True, rectangles[index2], node, node.point)
        else:

            temp = Node(False, rectangles[index], node, node.point)
            node.directions[index] = temp
            self.split_node(node.directions[index], rectangles[index], point)
        node.point = None
        return node

    def point_search(self, node: Node, rec: Rectangle, point: Point):

        index = axis(rec, point)

        if node.isleaf() and node.is_root:

            return node.point.data

        if node.directions[index].isleaf():
            if node.directions[index].point is not None:
                return node.directions[index].point.data
            return None

        else:

            return self.point_search(node.directions[index], node.directions[index].rec, point)

    def range_search(self, node: Node, drec: Rectangle):
        result = []
        if node.is_root and node.isleaf():
            return node.point.data
        if node.isleaf():

            if drec.overlaps_point(node.point):
                return node.point.data
        else:
            for i in range(0, 4):
                if node.directions[i].rec.overlaps(drec):
                    if node.directions[i].point is None and node.directions[i].isleaf():
                        continue
                    result.extend(self.range_search(node.directions[i], drec))
        return result


def axis(rec: Rectangle, point: Point):

    x_axis = rec.center().x < point.x
    y_axis = rec.center().y > point.y
    index = 2 * int(x_axis) + int(y_axis)

    return index


if __name__ == '__main__':

    df = pd.read_csv("data.txt", sep=" ", header=None)

    x_max = ord(df[0].max())
    x_min = ord(df[0].min())
    y_max = df[1].max()
    y_min = df[1].min()
    low_point = Point(x_min, y_min)
    high_point = Point(x_max, y_max)
    rect = Rectangle(low_point, high_point)

    qt = QuadTree(rect)

    for pd in range(len(df)):
        p = Point(ord(df[0][pd]),  df[1][pd], pd)
        qt.insert(p)

    fl = qt.point_search(qt.root, qt.rec, Point(ord('a'), 2))
    print(fl)
    data_rec = Rectangle(Point(ord('a'), 1), Point(ord('c'), 3))
    rs = qt.range_search(qt.root, data_rec)
    print(rs)

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

    def x_median(self):
        return (self.high.x + self.low.x)/2

    def y_median(self):
        return (self.high.y + self.low.y)/2

    def center(self):
        return Point(self.x_median(), self.y_median())

    def overlaps_point(self, point: Point):
        return self.low.x <= point.x <= self.high.x and self.low.y <= point.y <= self.high.y


class Node:

    def __init__(self, is_leaf, rec: Rectangle, parent: 'Node' = None, point=None):
        self.is_leaf = is_leaf
        self.parent = parent
        self.point = point
        # self.NW, self.NE, self.SW, self.SE = None, None, None, None
        self.directions = [None, None, None, None]
        self.rec = rec
    def is_root(self):
        return self.parent is None

    def all_leaves(self):
        for i in self.directions:
            if i.is_leaf == False:
                return False
        return True

def new_node(isleaf, point):
    return Node(isleaf, point)


class QuadTree:

    def __init__(self, rec: Rectangle):
        self.rec = rec
        self.root = Node(True, rec)

    def insert(self, point: Point):
        # if not self.rec.has_point(point):
        #     exit(-1)
        node = self.root
        while node.all_leaves() or node.is_root():
            if node.is_leaf:
                if node.point is None:
                    node.point = point
                    return

                else:
                    node = self.splitnode(node, point)
                    return
            else:
                for child_node in node.directions:
                    if child_node.rec.overlaps_point(point):
                        node = child_node

    def splitnode(self, node: Node, point: Point):
        rec: Rectangle = None
        x_axis = node.rec.center().x < point.x
        y_axis = node.rec.center().y > point.y
        index = 2*x_axis + y_axis

        x_axis2 = node.rec.center().x < node.point.x
        y_axis2 = node.rec.center().y > node.point.y
        index2 = 2 * x_axis2 + y_axis2

        rectangles = []
        p1 = Point(node.rec.low.x, node.rec.center().y)
        p2 = Point(node.rec.center().x, node.rec.high.y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(node.rec.low.x, node.rec.low.y)
        p2 = Point(node.rec.center().x, node.rec.center().y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(node.rec.center().x, node.rec.center().y)
        p2 = Point(node.rec.high.x, node.rec.high.y)
        rectangles.append(Rectangle(p1, p2))

        p1 = Point(node.rec.center().x, node.rec.low.y)
        p2 = Point(node.rec.high.x, node.rec.center().y)
        rectangles.append(Rectangle(p1, p2))

        if index != index2:
            node.directions[index] = Node(True, rectangles[index], node, point)
            node.directions[index2] = Node(True, rectangles[index2], node, node.point)
        else:
           node = self.splitnode(node, point)

        for i in range(0, 4):
            if i != index and i != index2:
                node.directions[i] = Node(True, rectangles[i], node, None)

        return node



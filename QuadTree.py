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
        self.directions: list= [None, None, None, None]
        self.rec = rec
    def is_root(self):
        return self.parent is None

    def all_leaves(self):
        if not self.is_root():
            for i in self.directions:
                if i.is_leaf is False:
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
        loop_check = 0
        node = self.root
        while loop_check == 0:
            if node.is_leaf:
                if node.point is None:
                    node.point = point
                    loop_check += 1
                else:
                    node = self.splitnode(node, node.rec, point)
                    loop_check += 1
            else:
                for child_node in node.directions:
                    if child_node.rec.overlaps_point(point):
                        node = child_node

    def splitnode(self, node: Node, rec: Rectangle, point: Point):

        x_axis = rec.center().x < point.x
        y_axis = rec.center().y > point.y
        index = 2*int(x_axis) + int(y_axis)

        x_axis2 = rec.center().x < node.point.x
        y_axis2 = rec.center().y > node.point.y
        index2 = 2 * int(x_axis2) + int(y_axis2)

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
        print("index1")
        print(index)
        print("index2")
        print(index2)
        if index != index2:
            node.directions[index] = Node(True, rectangles[index], node, point)
            node.directions[index2] = Node(True, rectangles[index2], node, node.point)
        else:
            print("trexw")
            temp = Node(False, rectangles[index], node, node.point)
            node.directions[index] = temp
            self.splitnode(node.directions[index], rectangles[index], point)
        node.point = None
        return node


low = Point(65,0)
high = Point(90, 12)

point_list = []
point_list.append(Point(75, 3))
point_list.append(Point(67, 5))
point_list.append(Point(70, 10))
point_list.append(Point(71, 5))
point_list.append(Point(74, 9))
point_list.append(Point(80, 3))

rect = Rectangle(low, high)
qt = QuadTree(rect)

qt.insert(point_list[0])
qt.insert(point_list[1])

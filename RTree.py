
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, low: Point, high: Point):
        self.low = low
        self.high = high


class Node:
    def __init__(self, is_leaf, entries, parent: 'Node' = None):  # type annotations
        self.is_leaf = is_leaf
        self.entries = entries  # exei metaksi m kai M entries
        self.parent = parent


class Entry:  # kathe entry exei onoma-child pointer h data name kai to rectangle toy
    def __init__(self, rec: Rectangle, child_p: Node, data_p):
        self.rec = rec
        self.data = data_p
        self.child = child_p


class RTree:
    def __init__(self, maximum, minimum):
        self.max = maximum
        self.min = minimum
        self.root = Node(True, None)  # kathe rtree exei ena root


with open('data.txt', 'r') as f:
    lines = f.readlines()


data = []
for line in lines:
    data.append([int(v) for v in line.split()])

# edw ton kwdika exontas dhmiourghsei ena rtree pernoyme to mix max kai kanoyme antistoixa group ta rectangles?
Points = []
Rectangles = []
for i in range(len(data)):
    Points.append(Point(data[i][0], data[i][1]))
    Rectangles.append(Rectangle(Points[i], Points[i]))
    #  ena point ana rectangle gia arxh

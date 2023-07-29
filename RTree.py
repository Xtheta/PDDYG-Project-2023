from typing import List


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
        self.entries = entries or []  # exei metaksi m kai M entries
        self.parent = parent

    def _is_root(self):
        return self.parent is None


class Entry:  # kathe entry exei onoma-child pointer h data name kai to rectangle toy
    def __init__(self, rec: Rectangle, child_p: Node = None, data_p=None):
        self.rec = rec
        self.data = data_p
        self.child = child_p

    def __str__(self): # print gia kathe entry
        return "Name is = " + self.data +" Xmin= " + str(self.rec.low.x) + " Ymin= " \
            + str(self.rec.low.y) + " Xmax= " + str(self.rec.high.x)  + " Ymax= " + str(self.rec.high.y)


class RTree:
    def __init__(self, maximum, minimum):
        self.max = maximum
        self.min = minimum
        self.root = Node(True, None)  # kathe rtree exei ena root kai stin arxi einai leaf

    def insertion(self, rec: Rectangle, data_p):
        temp: Node = self.choose_leaf(self.root, rec, data_p)
        if temp is not None and len(temp.entries) <= self.max: # an dn einai gemato to node mas
            temp.entries.append(Entry(rec, None, data_p)) # bale sto node to object mas
            temp.is_leaf = False
    def search_tree(self):
        pass

    def choose_leaf(self, node: Node, rec: Rectangle, data_p):
        if node.is_leaf:
            return node

        # exeis to entry kai to onoma kai /
        # p prepei na pas se ekeino to node
        #  choose node with criteria the least amount of change in its rectangle
        #  ties are to be resolved choosing rectangles with less area

    def find_least_area(self, entries: List[Entry], rec):
    # perinountai kanonika ta entries

    def pick_seeds(self):
        pass

    def adjust_tree(self):
        pass



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
r = RTree(5, 1)
r.insertion(Rectangles[0], 'a')
r.insertion(Rectangles[0], 'b')
r.insertion(Rectangles[0], 'b')
print(r.root.entries[0])

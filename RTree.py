from typing import List


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

    def changed_rectangle(self, rec: 'Rectangle'):

        return Rectangle(
            Point(min(self.low.x, rec.low.x), min(self.low.y, rec.low.y)),
            Point(max(self.high.x, rec.high.x), max(self.high.y, rec.high.y))
        )


class Node:
    def __init__(self, is_leaf, entries, parent: 'Node' = None):  # type annotations
        self.is_leaf = is_leaf
        self.entries = entries or []  # exei metaksi m kai M entries
        self.parent = parent

    def is_root(self):
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
        """
            if temp.is_root() and len(temp.entries)<=2:
            temp.entries.append(Entry(rec, None, data_p))

        if temp is not None and len(temp.entries) <= self.max: # an dn einai gemato to node mas
            temp.entries.append(Entry(rec, None, data_p)) # bale sto node to object mas
            temp.is_leaf = False
        """
        temp: Node = self.choose_leaf(self.root, rec, data_p)
        entry = Entry(rec, data_p=data_p)
        temp.entries.append(entry)

    def search_tree(self):
        pass

    def choose_leaf(self, node: Node, rec: Rectangle, data_p):

        while not node.is_leaf:
            entry = find_least_area(node.entries, rec)
            node = entry.child
        # exeis to entry kai to onoma kai /
        # p prepei na pas se ekeino to node
        #  choose node with criteria the least amount of change in its rectangle
        #  ties are to be resolved choosing rectangles with less area
        return node
    def pick_seeds(self):
        pass

    def adjust_tree(self):
        pass


def find_least_area(entries: List[Entry], rec: Rectangle):

    areas = [child.rec.area() for child in entries]
    enlargements = [rec.changed_rectangle(child.rec).area() - areas[j] for j, child in enumerate(entries)]
    min_enlargement = min(enlargements)
    instances = find_indices(enlargements, min_enlargement)
    if len(instances) == 1:
        return entries[instances[0]]
    else:
        min_area = min([areas[i] for i in instances])
        i = areas.index(min_area)
        return entries[i]


def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

with open('data.txt', 'r') as f:
    lines = f.readlines()


data = []
for line in lines:
    data.append([int(v) for v in line.split()])

# edw ton kwdika exontas dhmiourghsei ena rtree pernoyme to mix max kai kanoyme antistoixa group ta rectangles?
Points = []
Rectangles = []
for pd in range(len(data)):
    Points.append(Point(data[pd][0], data[pd][1]))
    Rectangles.append(Rectangle(Points[pd], Points[pd]))
    #  ena point ana rectangle gia arxh
r = RTree(5, 1)
r.insertion(Rectangles[0], 'a')
r.insertion(Rectangles[1], 'b')
r.insertion(Rectangles[2], 'b')
print(r.root.entries[0])
print(r.root.entries[1])
print(r.root.entries[2])


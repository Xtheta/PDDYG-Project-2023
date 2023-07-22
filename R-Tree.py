
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, low: Point, high: Point):
        self.low = low
        self.high = high


class LeafEntry:
    def __init__(self, rec: Rectangle, leaf_id: int):
        self.rec = rec
        self.leaf_id = leaf_id


class Entry:
    def __init__(self, rec: Rectangle, leaf_id: int):
        self.rec = rec
        self.leaf_id = leaf_id


class LeafNode:
    def __init__(self, entries: LeafEntry, entries_sum: int):
        # may turn into a Node subclass
        self.entries = entries
        self.entries_sum = entries_sum


class Node:
    def __init__(self, is_leaf=True, entries=0, rectangle=Rectangle(Point(0, 0), Point(1, 1))):
        self.is_leaf = is_leaf
        self.entries = entries
        self.children = []
        self.mbr: Rectangle = rectangle


class RTree:
    def __init__(self, maximum, minimum):
        self.max = maximum
        self.min = minimum
        self.root = Node()

    def insert(self, entry):
        chosen_leaf = self.choose_leaf()
        chosen_leaf.children.append(entry) #peripou
        # den exoume thn periptwsh gia to root

    def choose_leaf(self):
        node = self.root
        if node.is_leaf:
            return node
        else:
            for F in node.children:
                pass  # choose node with criteria least amount of change in its rectangle
            # ties are to be resolved choosing rectangles with less area


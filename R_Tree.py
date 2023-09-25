import itertools
from typing import List, Optional
import math
import pandas as pd


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

    def area(self):
        return self.width * self.height

    def changed_rectangle(self, rec: 'Rectangle'):
        return Rectangle(
            Point(min(self.low.x, rec.low.x), min(self.low.y, rec.low.y)),
            Point(max(self.high.x, rec.high.x), max(self.high.y, rec.high.y))
        )

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

    def intersects(self, rec: 'Rectangle'):
        xmin = max(self.low.x, rec.low.x)
        ymin = max(self.low.y, rec.low.y)
        xmax = min(self.high.x, rec.high.x)
        ymax = min(self.high.y, rec.high.y)

        min_point = Point(xmin, ymin)
        max_point = Point(xmax, ymax)
        new_rec = Rectangle(min_point, max_point)
        return new_rec

    def contains(self, rec: 'Rectangle'):
        return self.low.x <= rec.low.x <= self.high.x and self.low.x <= rec.high.x <= self.high.x \
            and self.low.y <= rec.low.y <= self.high.y and self.low.y <= rec.high.y <= self.high.y


def union(rect1: Rectangle, rect2: Rectangle) -> Rectangle:
    if rect1 is None:
        return rect2
    if rect2 is None:
        return rect1
    return rect1.changed_rectangle(rect2)


def union_all(rects: List[Rectangle]) -> Rectangle:
    result = None
    for rect in rects:
        result = union(result, rect)  # MBR that contains all rectangles
    return result


class Node:
    def __init__(self, is_leaf, entries, parent: 'Node' = None):  # type annotations
        self.is_leaf = is_leaf
        self.entries = entries or []  # between m and M entries, except leaf Root
        self.parent = parent

    def is_root(self):
        return self.parent is None
    @property
    def parent_entry(self) -> Optional['Entry']:
        if self.parent is not None:
            return next(entry for entry in self.parent.entries if entry.child is self)
            # find and return given node as entry
        return None

    def get_bounding_rect(self):
        return union_all([entry.rec for entry in self.entries])


class Entry:  # each entry has its mbr and a child pointer (to nodes) or a data pointer ( data given at insertion)
    def __init__(self, rec: Rectangle, child_p: Node = None, data_p=None):
        self.rec = rec
        self.data = data_p
        self.child = child_p


class RTree:
    def __init__(self, maximum, minimum):
        self.M = maximum
        self.m = minimum
        self.root = Node(True, None)  # Each RTree has a root that is a leaf at time of construction

    def insertion(self, rec: Rectangle, data_p):

        temp: Node = self.choose_leaf(self.root, rec)  # we choose which node to insert to
        entry = Entry(rec, data_p=data_p)  # we create an entry with the given data and its MBR
        temp.entries.append(entry)

        split_node = None
        if len(temp.entries) > self.M:  # check if given entry limit is exceeded
            split_node = self.quadratic_split(temp)  # split our node into 2 and share our entries
        self.adjust_tree_strategy(temp, split_node)

    def search_tree(self, rec: Rectangle, node: Node = None):

        result = []
        if node is None:
            node = self.root  # starting point

        if not node.is_leaf:  # parse top down all entries to find any MBR in our search range
            for entry in node.entries:
                if entry.rec.overlaps(rec):
                    new_rec = entry.rec.intersects(rec)  # search its child nodes for the part of the MBR that overlaps
                    temp = self.search_tree(new_rec, entry.child)
                    if temp is not None:
                        result.extend(temp)  # with append we would have had [[], [], []], ...]
            return result

        if node.is_leaf:
            for entry in node.entries:
                if rec.contains(entry.rec):  # check if entry.rec is in completely in search range
                    result.append(entry.data)  # append data if its MBR overlaps
                # se ena Node
            return result  # we return the data ( in our case rows from our file)

    @staticmethod
    def choose_leaf(node: Node, rec: Rectangle):

        while not node.is_leaf:
            entry = find_least_area(node.entries, rec)
            node = entry.child
        # nodes are to be chosen by the least amount of change in its rectangle, if we were to proceed with a /
        # insert
        # Keep choosing that till you find a leaf node
        # Basically you choose the path in the R Tree with the smallest possible spatial change
        return node

    def perform_node_split(self, node: Node, group1: List[Entry], group2: List[Entry]) \
            -> Node:

        node.entries = group1  # Keep old node with first group, create a new one with same parent and 2nd entries group
        split_node = Node(node.is_leaf, parent=node.parent, entries=group2)  # keeps the leaf value of og node

        self._fix_children(split_node)

        return split_node

    @staticmethod
    def _fix_children(node: Node) -> None:  # for upper (non-leaf) levels of nodes
        if not node.is_leaf:
            for entry in node.entries:
                entry.child.parent = node

    def adjust_tree_strategy(self, node: Node, split_node: Node = None) -> None:

        while not node.is_root():
            parent = node.parent
            node.parent_entry.rec = union_all([entry.rec for entry in node.entries])
            # creates an MBR for all the entries of our node
            # MBR of a node is always at its parent
            if split_node is not None:
                rec = union_all([e.rec for e in split_node.entries])
                # creates an MBR for all the entries of our new node
                entry = Entry(rec, child_p=split_node)
                parent.entries.append(entry)
                # new Entry of the new node for the parent
                if len(parent.entries) > self.M:
                    split_node = self.quadratic_split(parent)
                    # possible split needed
                else:
                    split_node = None
            node = parent
        if split_node is not None:
            # if root got split or level 1 nodes got split and are over M
            self.grow_tree([node, split_node])

    def grow_tree(self, nodes: List[Node]):

        entries = [Entry(node.get_bounding_rect(), child_p=node) for node in nodes]
        # all entries that got split at Level 1
        self.root = Node(False, entries=entries)  # Pointer of root goes to the new node
        for node in nodes:
            node.parent = self.root
        return self.root

    def quadratic_split(self, node: Node):
        entries = node.entries[:]  # shallow list copy of our entries ( any changes don't apply to the original )
        seed1, seed2 = _pick_seeds(entries)  # surely split the 2 furthest apart entries to save space
        entries.remove(seed1)
        entries.remove(seed2)
        # we have now to decide what will happen with the rest M-1 nodes
        group1, group2 = ([seed1], [seed2])  # 2 groups, each one representing the entries of the old and new node
        rec1: Rectangle
        rec2: Rectangle
        rec1, rec2 = (seed1.rec, seed2.rec)  # MBRs of our 2 furthest apart entries

        num_entries = len(entries)  # M-1 entries
        while num_entries > 0:
            # Proceed to choose the best group to insert up until one of the two reaches the limit m \
            # then place all the remaining entries to the other group
            len1, len2 = (len(group1), len(group2))
            group1_underfull = len1 < self.m <= len1 + num_entries
            group2_underfull = len2 < self.m <= len2 + num_entries
            if group1_underfull and not group2_underfull:
                group1.extend(entries)
                break
            if group2_underfull and not group1_underfull:
                group2.extend(entries)
                break
            print("tr")
            # Find out which entry to insert next
            area1, area2 = rec1.area(), rec2.area()
            entry = _pick_next(entries, rec1, area1, rec2, area2)
            new_rec1, new_rec2 = rec1.changed_rectangle(entry.rec), rec2.changed_rectangle(entry.rec)
            # Finding which rectangle is closer to our entry
            gained_area1 = new_rec1.area() - area1  # potential gained area
            gained_area2 = new_rec2.area() - area2
            if gained_area1 == gained_area2:  # tie breaker 1
                if area1 == area2:
                    group = group1 if len1 <= len2 else group2  # fewer entries tie breaker 3
                else:
                    group = group1 if area1 < area2 else group2  # smallest area tie breaker 2
            else:
                group = group1 if gained_area1 < gained_area2 else group2
            group.append(entry)

            # Changed new rectangle gets pushed only into the added entry group
            if group is group1:
                rec1 = new_rec1
            else:
                rec2 = new_rec2
            # Update entries list
            entries.remove(entry)
            num_entries = len(entries)
        return self.perform_node_split(node, group1, group2)


def find_least_area(entries: List[Entry], rec: Rectangle):
    areas = [child.rec.area() for child in entries]  # list with rectangles for possible insert
    enlargements = [rec.changed_rectangle(child.rec).area() - areas[j] for j, child in enumerate(entries)]
    # rectangle englargement for each possible rectangle
    min_enlargement = min(enlargements)
    instances = find_indices(enlargements, min_enlargement)  # position of min possible rects
    if len(instances) == 1:
        return entries[instances[0]]
    else:
        min_area = min([areas[i] for i in instances])  # if more than one have the minimum value
        i = areas.index(min_area)  # list with their original rec area
        return entries[i]   # and choose that, otherwise the first is chosen


def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)  # finding positions of an instance and its duplicates in a list
    return indices


def _pick_seeds(entries: List[Entry]) -> (Entry, Entry):
    seeds = None
    max_wasted_area = None
    e1: Entry
    e2: Entry
    for e1, e2 in itertools.combinations(entries, 2):  # choose a pair of 2 out of our entries
        combined_rect = e1.rec.changed_rectangle(e2.rec)  # new MBR for combined rectangles
        wasted_area = combined_rect.area() - e1.rec.area() - e2.rec.area()
        if max_wasted_area is None or wasted_area > max_wasted_area:
            max_wasted_area = wasted_area  # split the 2 furthest apart entries judging by the potential wasted space
            seeds = (e1, e2)
    return seeds


def _pick_next(remaining_entries: List[Entry],
               group1_rect: Rectangle,
               group1_area: float,
               group2_rect: Rectangle,
               group2_area: float) -> Entry:
    max_diff = None
    result = None
    for e in remaining_entries:
        d1 = group1_rect.changed_rectangle(e.rec).area() - group1_area  # gained area
        d2 = group2_rect.changed_rectangle(e.rec).area() - group2_area  # gained area
        diff = math.fabs(d1 - d2)
        # diff near zero if entry is far from both rectangles (d1 - d2 =0)
        # while an entry gets closer, diff has linear growth
        if max_diff is None or diff > max_diff:  # choose the entry with the max diff in its rectangle
            max_diff = diff
            result = e
    return result


if __name__ == '__main__':
    df = pd.read_csv("data.txt", sep=" ", header=None)

    r = RTree(4, 2)

    for pd in range(len(df)):
        # data_rec = Rectangle(Point(ord(df[0][pd]), df[1][pd]), Point(ord(df[0][pd]), df[1][pd]))
        data_rec = Rectangle(Point(ord(df[0][pd]), df[1][pd]), Point(ord(df[0][pd]), df[1][pd]))
        r.insertion(data_rec, pd)

    a = r.search_tree(Rectangle(Point(ord('a'), 1), Point(ord('i'), 5)))
    print(f"{len(a)} matches were found :")
    print(a)
    print(df.iloc[a])

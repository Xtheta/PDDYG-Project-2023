import itertools
from typing import List, Optional
import math
import time
import pandas as pd


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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

    def area(self) -> float:
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


def union(rect1: Rectangle, rect2: Rectangle) -> Rectangle:
    if rect1 is None:
        return rect2
    if rect2 is None:
        return rect1
    return rect1.changed_rectangle(rect2)


def union_all(rects: List[Rectangle]) -> Rectangle:
    result = None
    for rect in rects:
        result = union(result, rect)  # to mbr pou periexei ola ta rectangles
    return result


class Node:
    def __init__(self, is_leaf, entries, parent: 'Node' = None):  # type annotations
        self.is_leaf = is_leaf
        self.entries = entries or []  # exei metaksi m kai M entries
        self.parent = parent

    def is_root(self):
        return self.parent is None

    @property
    def parent_entry(self) -> Optional['Entry']:
        if self.parent is not None:
            return next(entry for entry in self.parent.entries if entry.child is self)
            # vres to node san entry kai pisw
        return None

    def get_bounding_rect(self):
        return union_all([entry.rec for entry in self.entries])


class Entry:  # kathe entry exei onoma-child pointer h data name kai to rectangle toy
    def __init__(self, rec: Rectangle, child_p: Node = None, data_p=None):
        self.rec = rec
        self.data = data_p
        self.child = child_p

    def __str__(self):  # print gia kathe entry
        return "Name is at line " + str(self.data) + " Its MBR has (Xmin,Ymin) = (" + chr(self.rec.low.x) + ", " \
            + str(self.rec.low.y) + ") and (Xmax,Ymax) = (" + chr(self.rec.high.x) + ", " + str(self.rec.high.y) + ")"

    @property
    def is_leaf(self):
        return self.child is None


class RTree:
    def __init__(self, maximum, minimum):
        self.M = maximum
        self.m = minimum
        self.root = Node(True, None)  # kathe rtree exei ena root kai stin arxi einai leaf

    def insertion(self, rec: Rectangle, data_p):
        """
            if temp.is_root() and len(temp.entries)<=2:
            temp.entries.append(Entry(rec, None, data_p))

        if temp is not None and len(temp.entries) <= self.max: # an dn einai gemato to node mas
            temp.entries.append(Entry(rec, None, data_p)) # bale sto node to object mas
            temp.is_leaf = False
        """
        temp: Node = self.choose_leaf(self.root, rec)
        entry = Entry(rec, data_p=data_p)
        temp.entries.append(entry)

        split_node = None
        if len(temp.entries) > self.M:
            split_node = quadratic_split(self, temp)
        self.adjust_tree_strategy(temp, split_node)
        #  if len(temp.entries) > self.M:

    def search_tree(self, rec: Rectangle, node: Node = None):

        result: list[int] = []
        if node is None:
            node = self.root

        if not node.is_leaf:
            for entry in node.entries:
                if entry.rec.overlaps(rec):
                    new_rec = entry.rec.intersects(rec)
                    print("new")
                    print(new_rec)
                    temp = self.search_tree(new_rec, entry.child)
                    #  den afhneis to rec idio vaseis ton yposynolo-tomh
                    if temp is not None:
                        result.extend(temp)
            return result

        if node.is_leaf:  # oxi parentheseis dn einai synarthiseis
            for entry in node.entries:
                if entry.rec.overlaps(rec):
                    result.append(entry.data)  # den kanoyme apeytheias return epeidh mporoume na vroymme pollapla
                # se ena Node
            return result  # vriskoume tis grammes sta opoia yparxoyn ta names poy theloyme

    @staticmethod
    def choose_leaf(node: Node, rec: Rectangle):

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

    def perform_node_split(self, node: Node, group1: List[Entry], group2: List[Entry]) \
            -> Node:
        """
        Splits a given node into two nodes. The original node will have the entries specified in group1, and the
        newly-created split node will have the entries specified in group2. Both the original and split node will
        have their children nodes adjusted. so they have the correct parent.
        :param node: Original node to split
        :param group1: Entries to assign to the original node
        :param group2: Entries to assign to the newly-created split node
        :return: The newly-created split node
        """
        node.entries = group1  # κραταμε το group1 kai φτιαχνουμε ενα node που ειναι leaf έχει το ιδιο parent
        split_node = Node(node.is_leaf, parent=node.parent, entries=group2)  # kai entities to group2
        self._fix_children(node)
        self._fix_children(split_node)
        return split_node

    @staticmethod
    def _fix_children(node: Node) -> None:
        if not node.is_leaf:  # ean den einai leaf
            for entry in node.entries:
                entry.child.parent = node

    def adjust_tree_strategy(self, node: Node, split_node: Node = None) -> None:
        """
        Ascend from a leaf node to the root, adjusting covering rectangles and propagating node splits as necessary.
        """
        while not node.is_root():
            parent = node.parent
            node.parent_entry.rec = union_all([entry.rec for entry in node.entries])
            # mbr pou periexei ola aytwn twn paidiwn tou
            # h klhsh sto parent_entry ginetai gia na exoume to node mas ws entry
            # epeidh ta stoixeia enos node perigrafontai panta ston gonea toy
            if split_node is not None:  # an egine splitting
                rec = union_all([e.rec for e in split_node.entries])
                # to mbr twn entries pou pigan sto kainourgio mas node
                entry = Entry(rec, child_p=split_node)
                # neo entry me to mbr poy perigrafei to neo node mas
                parent.entries.append(entry)
                # dwse sto gonea tou node mas to paidi toy
                if len(parent.entries) > self.M:
                    split_node = quadratic_split(self, parent)
                    # ama ksepernaei ta M paidia kane split
                else:
                    split_node = None
            node = parent
        if split_node is not None:
            # ama egine spltting gonea
            self.grow_tree([node, split_node])

    def grow_tree(self, nodes: List[Node]):
        """
        Grows the R-Tree by creating a new root node, with the given nodes as children.
        :param nodes: Existing nodes that will become children of the new root node.
        :return: New root node
        """

        entries = [Entry(node.get_bounding_rect(), child_p=node) for node in nodes]
        # lista entries me ta mbr tou palio kai neoy node ( split_node )
        self.root = Node(False, entries=entries)  # PROSOXH EDW AN MPAINEI H LISTA
        # ftiaxnoume dld mbr gia ta panw panw
        for node in nodes:
            node.parent = self.root
        return self.root


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


def quadratic_split(tree: RTree, node: Node):
    entries = node.entries[:]  # copy tis listas kata value poy oi allages den pernane
    seed1, seed2 = _pick_seeds(entries)  # dio entries ta opoia meta petame apo tin lista mas
    entries.remove(seed1)
    entries.remove(seed2)
    group1, group2 = ([seed1], [seed2])  # dio listes group1 kai group2 pou to kathena exei antistoixa to seed1 kai 2
    rec1: Rectangle
    rec2: Rectangle
    rec1, rec2 = (seed1.rec, seed2.rec)  # pleiades gia na glytwsoume xwro apparently
    num_entries = len(entries)  # ta entries moy sto node pera apo ta dio p eksetasame
    while num_entries > 0:
        # If one group has so few entries that all the rest must be assigned to it in order for it to meet the
        # min_entries requirement, assign them and stop. (If both groups are underfull, then proceed with the
        # algorithm to determine the best group to extend.)
        len1, len2 = (len(group1), len(group2))
        group1_underfull = len1 < tree.m <= len1 + num_entries
        group2_underfull = len2 < tree.m <= len2 + num_entries
        if group1_underfull and not group2_underfull:
            group1.extend(entries)
            break
        if group2_underfull and not group1_underfull:
            group2.extend(entries)
            break
        # Pick the next entry to assign
        area1, area2 = rec1.area(), rec2.area()
        entry = _pick_next(entries, rec1, area1, rec2, area2)
        # Add it to the group whose covering rectangle will have to be enlarged the least to accommodate it.
        # Resolve ties by adding the entry to the group with the smaller area, then to the one with fewer
        # entries, then to either.
        new_rec1, new_rec2 = rec1.changed_rectangle(entry.rec), rec2.changed_rectangle(entry.rec)
        # nea rectangles
        gained_area1 = new_rec1.area() - area1  # το area poy παρθηκε
        gained_area2 = new_rec2.area() - area2
        if gained_area1 == gained_area2:  # εαν παρουν το ιδιο
            if area1 == area2:
                group = group1 if len1 <= len2 else group2  # smaller entries tie braker
            else:
                group = group1 if area1 < area2 else group2  # smallest area tie braker
        else:
            group = group1 if gained_area1 < gained_area2 else group2
        group.append(entry)
        # Update the winning group's covering rectangle
        if group is group1:  # update sto rectangle pou exoume ektos listas giati ekeino einai to teliko
            rec1 = new_rec1
        else:
            rec2 = new_rec2
        # Update entries list
        entries.remove(entry)
        num_entries = len(entries)  # posa exoun meinei gia tin sinthiki toy while
    return tree.perform_node_split(node, group1, group2)


def _pick_seeds(entries: List[Entry]) -> (Entry, Entry):
    seeds = None
    max_wasted_area = None
    e1: Entry
    e2: Entry
    for e1, e2 in itertools.combinations(entries, 2):  # ola ta entries ana duio
        combined_rect = e1.rec.changed_rectangle(e2.rec)  # dhmiourgoume to mbr gia ta entry mas
        wasted_area = combined_rect.area() - e1.rec.area() - e2.rec.area()  # posos xwros xalietai = d =d1 -d2
        if max_wasted_area is None or wasted_area > max_wasted_area:  # vriskoume to d max
            max_wasted_area = wasted_area  # gia na kanoume split ekei
            seeds = (e1, e2)  # pleiada
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
        diff = math.fabs(d1 - d2)  # epilogh toy entry poy einai pio konta sto ena apo ta dio rectangle mas
        # an htan makria kai apo ta dio to d1-d2 tha plisiaze to 0 , omws otan einai pio konta sto ena
        # tha fanei sth diafora tous
        if max_diff is None or diff > max_diff:  # epilegoyme
            max_diff = diff
            result = e
    return result


if __name__ == '__main__':
    df = pd.read_csv("data.txt", sep=" ", header=None)

    # # edw ton kwdika exontas dhmiourghsei ena rtree pernoyme to mix max kai kanoyme antistoixa group ta rectangles?
    t1 = time.time()
    r = RTree(4, 2)

    for pd in range(len(df)):
        # data_rec = Rectangle(Point(ord(df[0][pd]), df[1][pd]), Point(ord(df[0][pd]), df[1][pd]))
        data_rec = Rectangle(Point(ord(df[0][pd]), df[1][pd]), Point(ord(df[0][pd]), df[1][pd]))
        r.insertion(data_rec, pd)

    a = r.search_tree(Rectangle(Point(ord('a'), 1), Point(ord('i'), 5)))

    print(f"{len(a)} matches were found :")
    print(a)
    print(df.iloc[a])

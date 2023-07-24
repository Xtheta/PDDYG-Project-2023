import math
import pprint
import csv
pp = pprint.PrettyPrinter(indent=4)


#LOAD DATA FROM CSV FILE
#THE DATABASE FEATURES THE SURNAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 
surnames = []
awards = []
education = []

with open("computer_scientists.csv", 'r') as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        surnames.append(row[0])
        awards.append(row[1])
        education.append(row[2])

awards = [eval(i) for i in awards]      # eval() parses the expression passed to this method and runs python expression within the program
award_max=max(awards)

first_letter = []                               # The first_letter list holds the first letter of each computer scientist's surname
for x in range(len(surnames)):
    first_letter.append(ord(surnames[x][0]))    # ord() returns the Unicode code from a given character

data = list(zip(first_letter,awards))           # Combine the first_letter and awards lists
#print(data)



#CREATING A LIST OF NODES 
class Node:
    def __init__(self, point, surname, award, education):
        self.point = point
        self.surname = surname
        self.award = award
        self.education = education
        self.left = None
        self.right = None

def newNode(point, surname, award, education):
    return Node(point, surname, award, education)

nodeList = []
for x in range(len(data)):
    new_node=newNode(data[x], surnames[x], awards[x], education[x])
    nodeList.append(new_node)



#BUILDING 2D KD TREE
k=2
def build_kdtree(node_list, depth=0):
    n = len(node_list)
    if n <= 0:
        return None

    axis = depth % k                                        # Calculating current axis of comparison
    node_list.sort(key=lambda node: node.point[axis])       # Sorting nodes by axis-value of each point
    node = newNode(None, None, None, None)

    node = node_list[n//2]                                  # The spliting point will be the median 
    node.left = build_kdtree(node_list[:n // 2], depth+1)
    node.right = build_kdtree(node_list[n // 2 + 1:], depth+1)

    return node

kd_tree = build_kdtree(nodeList)


#PRINTING AND SEARCHING FUNCTIONS
def print_kdtree(kd_tree, n):
    if kd_tree is None:
        return
    
    print(n,". Point is:", kd_tree.point, kd_tree.surname, kd_tree.award, kd_tree.education)
    if kd_tree.left != None:
        print(n,". Left Subtree")
        print_kdtree(kd_tree.left,n+1)
    if kd_tree.right != None:
        print(n,". Right Subtree")
        print_kdtree(kd_tree.right, n+1)

print_kdtree(kd_tree,0)


def samePoints(point1, point2):
    for i in range(k):
        if point1[i] != point2[i]:              # Both x and y value must be equal
            return False
    return True

def kdtree_search(root, point, depth=0):        # Useful for searching a single node
    if root is None:
        return False
    if samePoints(root.point, point):
        return True

    axis = depth % k
    if point[axis]<root.point[axis]:
        return kdtree_search(root.left, point, depth+1)
    return kdtree_search(root.right, point, depth+1)




# 1D RANGE SEARCH FUNCTION
def FindSplitNode(root, p_min , p_max, dim):

    '''
    Searches for a common node that splits the range
    Arguments:
        p_min       : Starting range 
        p_max       : Ending range 
        dim         : x or y
    '''
    
    splitnode = newNode(None, None, None, None)
    splitnode = root
    while splitnode != None:
        if p_max < splitnode.point[dim]:
            splitnode = splitnode.left
        elif p_min > splitnode.point[dim]:
            splitnode = splitnode.right
        elif p_min <= splitnode.point[dim] <= p_max :
            break
    return splitnode

#print(FindSplitNode(kd_tree, 65, 66, 0).point)



def withinRange(point, range , check):

    '''
    Checks if the value of node is within the required range
    Arguments:
        point       : A point in tree
        range       : A list containing range to be checked with
        check       : specifies which option should be performed
    '''

    # 1 DIMENSION
    if check == 1:
        x = point
        if (x >= range[0][0]  and x <= range[0][1] ) :
            return True
        else:
            return False
        
    # 2 DIMENSIONS
    elif check == 2:
        x = point[0]
        y = point[1]

        if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
            return True
        else:
            return False


def SearchRangeTree1d (root, p1, p2, dim):
    '''
    Performs 1D range search
    Arguments:
        root        : The tree's root
        p1          : Starting range 
        p2          : Ending range 
        dimension   : x-axis or y-axis
    '''
    nodes = []
    splitnode = FindSplitNode(root , p1, p2, dim)                    # Find the node which the least common ancestor in the tree for given range
    
    if splitnode == None:
        return nodes
    elif withinRange( splitnode.point[dim] , [(p1, p2)], 1):         # Check if the node is a valid node in range
        nodes.append(splitnode.point)

    nodes += SearchRangeTree1d(splitnode.left, p1, p2, dim)          # Search for nodes in left subtree
    nodes += SearchRangeTree1d(splitnode.right, p1, p2, dim)         # Search for nodes in right subtree
    return nodes

#print(SearchRangeTree1d(kd_tree, 70, 80, 0))



# 2D RANGE SEARCH FUNCTION 

def SearchRangeTree2d (root, x1, x2, y1, y2):
    '''
    Performs 2D range search
    Arguments:
        root        : The tree's root
        x1          : Starting range for x-coord
        x2          : Ending range for x-coord
        y1          : Starting range for y-coord
        y2          : Ending range for y-coord
    '''
    results = []
    splitnode = FindSplitNode(root, x1, x2, 0)

    if (splitnode == None):
        return results
    elif withinRange(splitnode.point, [(x1, x2), (y1, y2)], 2) :
        results.append(splitnode.point)
        
        vl = splitnode.left                                             # Traverse the nodes in left child of split node
        while ( vl != None ):
            if withinRange(vl.point, [(x1, x2), (y1, y2)], 2):          # Check if the node is a valid node in range
                results.append(vl.point)
            if (x1 <= vl.point[0]):                                     # Search the associated ytree at the left child of current node in xtree
                if vl.right != None:
                    results += SearchRangeTree1d(vl.right, y1, y2, 0)
                vl = vl.left
            else:
                vl = vl.right

        vr = splitnode.right                                            # Traverse the nodes in right child of split node
        while ( vr != None ):
            if withinRange(vr.point, [(x1, x2), (y1, y2)], 2):          # Check if the node is a valid node in range
                    results.append(vr.point)
            if ( x2 >= vr.point[0] ):                                   # Search the associated ytree at the left child of current node in xtree
                if vr.left != None:
                    results += SearchRangeTree1d(vr.left, y1, y2, 0)
                vr = vr.right
            else:
                    vr = vr.left
        
        return results

print(SearchRangeTree2d(kd_tree, 70, 75, 2, 4))


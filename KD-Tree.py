import math
import pprint
import csv
pp = pprint.PrettyPrinter(indent=4)


#LOAD DATA FROM CSV FILE
#THE DATABASE FEATURES THE SURNAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 
surnames = []
awards = []
education = []

""""
with open("scientists.csv", 'r', newline = '', encoding="utf-8") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        surnames.append(row[0][1:-1])
        awards.append(row[1])
        education.append(row[2])
"""""


with open("kdtree_example_set.csv", 'r') as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        surnames.append(row[0])
        awards.append(row[1])
        education.append(row[2])

awards = [eval(i) for i in awards]      # eval() parses the expression passed to this method and runs python expression within the program
award_max=max(awards)
#print(award_max)

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
        self.isLeaf = False

def newNode(point, surname, award, education):
    return Node(point, surname, award, education)

nodeList = []
for x in range(len(data)):
    new_node=newNode(data[x], surnames[x], awards[x], education[x])
    nodeList.append(new_node)

nodeList.sort(key=lambda node: node.point)



#BUILDING 2D KD TREE
k=2
def build_kdtree(node_list, depth=0):
    n = len(node_list)
    if n <= 0:
        return None
    

    axis = depth % k                                                         # Calculating current axis of comparison
    sorted_list = []
    sorted_list = sorted(node_list, key=lambda node: node.point[axis])       # Sorting nodes by axis-value of each point
    node = newNode(None, None, None, None)


    node = sorted_list[n//2]                                                 # The spliting point will be the median 
    if n == 1:
        node.isLeaf = True
    node.left = build_kdtree(sorted_list[:n // 2], depth+1)
    node.right = build_kdtree(sorted_list[n // 2 + 1:], depth+1)

    return node

kd_tree = build_kdtree(nodeList)


#PRINTING AND SEARCHING FUNCTIONS
def print_kdtree(kd_tree, n):
    if kd_tree is None:
        return
    
    print(n,". Point is:", kd_tree.point, kd_tree.surname, kd_tree.award, kd_tree.education, kd_tree.isLeaf)
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
    if root == None:
        return nodes
    elif withinRange( root.point[dim] , [(p1, p2)], 1):         # Check if the node is a valid node in range
        nodes.append(root.point)
    
    nodes += SearchRangeTree1d(root.left, p1, p2, dim)          # Search for nodes in left subtree
    nodes += SearchRangeTree1d(root.right, p1, p2, dim)         # Search for nodes in right subtree
    return nodes

#print(SearchRangeTree1d(kd_tree, 68, 71, 0))



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
    #splitnode = FindSplitNode(root, x1, x2, 0)

    if (root == None):
        return results
    elif withinRange(root.point, [(x1, x2), (y1, y2)], 2) :          # Check if the node is a valid node in range
        results.append(root.point)
    
    results += SearchRangeTree2d(root.left, x1, x2, y1, y2)          # Search for nodes in left subtree
    results += SearchRangeTree2d(root.right, x1, x2, y1, y2)         # Search for nodes in right subtree
        
    return results

print(SearchRangeTree2d(kd_tree, 65, 72, 2, award_max))


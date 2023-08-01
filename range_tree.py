import time
import pprint
import csv
import pandas
pp = pprint.PrettyPrinter(indent=4)

#LOAD DATA FROM CSV FILE
surnames = []
awards = []
education = []


with open("kdtree_example_set.csv", 'r') as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        surnames.append(row[0])
        awards.append(row[1])
        education.append(row[2])

""""
with open("scientists.csv", 'r', newline = '', encoding="utf-8") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        surnames.append(row[0][1:-1])
        awards.append(row[1])
        education.append(row[2])

     """   

awards = [eval(i) for i in awards]
award_max=max(awards)
first_letter = []
for x in range(len(surnames)):
    first_letter.append(ord(surnames[x][0]))

data = list(zip(first_letter,awards))   #combine the lists
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
        self.assoc = None

def newNode(point, surname, award, education):
    return Node(point, surname, award, education)

nodeList = []
for x in range(len(data)):
    new_node=newNode(data[x], surnames[x], awards[x], education[x])
    nodeList.append(new_node)

nodeList.sort(key=lambda node: node.point)
#for x in range(len(nodeList)):
   # print(nodeList[x].point)

#BUILDING 1D RANGE TREE
def build_range_tree(node_list):
    if not node_list:
        return None
     
    root = newNode(None, None, None, None)
    mid_val = len(node_list)//2
    root = node_list[mid_val] 

    root.left = build_range_tree(node_list[:mid_val])
    root.right = build_range_tree(node_list[mid_val+1:])
        
    return root

#BUILDING 2D RANGE TREE
def build_range_tree2(node_list):
    if not node_list:
        return None
     
    node = newNode(None, None, None, None)
    mid_val = len(node_list)//2
    node = node_list[mid_val]  
    if len(node_list)==1:
       node.isLeaf = True

    node.left = build_range_tree2(node_list[:mid_val])
    node.right = build_range_tree2(node_list[mid_val+1:])
    node.assoc = build_range_tree(node_list)                     #a bst for every node ordered by y-coordinates
       
    return node

range_tree=build_range_tree2(nodeList)                           # a bst ordered by x-coordinates




def print_range_tree(range_tree, n):
    if range_tree is None:
        return
    
    print(n,". Point is:", range_tree.point, range_tree.surname, range_tree.award, range_tree.education, range_tree.isLeaf)
    if range_tree.left != None:
        print(n,". Left Subtree")
        print_range_tree(range_tree.left,n+1)
    if range_tree.right != None:
        print(n,". Right Subtree")
        print_range_tree(range_tree.right, n+1)
#print_range_tree(range_tree,0)



def withinRange(point, range , check):

    '''
    Checks if the value of node is within the required range
    Arguments:
        point       : A point in tree
        range       : A list containing range to be checked with
        check       : specifies which option should be performed
    Returns :
        True if in range else False
    '''

    if check == 1:
        x = point
        if (x >= range[0][0]  and x <= range[0][1] ) :
            return True
        else:
            return False
    elif check == 2:
        x = point[0]
        y = point[1]

        if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
            return True
        else:
            return False
        
def getValue (node, enable):

    '''
    Reads the desired value from node
    Arguments:
        point       : A point in tree
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
    '''
    if enable:
        value = node.point[0]
    else:
        value = node.point[1]
    return value


def FindSplitNode(root, p_min , p_max, enable):

    '''
    Searches for a common node that splits the range
    Arguments:
        root        : The tree's root
        p_min       : Starting range 
        p_max       : Ending range 
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
    Returns : A Node
    '''

    splitnode = newNode(None, None, None, None)
    splitnode = root
    while splitnode != None:
           node = getValue(splitnode, enable)
           if p_max < node:
                splitnode = splitnode.left
           elif p_min > node:
                splitnode = splitnode.right
           elif p_min <= node <= p_max:
                break
    return splitnode

unique_sur = []

def SearchRangeTree1d (root, p1, p2, enable = True):
    '''
    Performs 1D range search
    Arguments:
        root        : A Node in tree
        p1          : Starting range 
        p2          : Ending range 
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
    '''
    nodes = []
    splitnode = FindSplitNode(root , p1, p2, enable)               # find the node which the least common ancestor in the tree for given range
    
    if splitnode == None:
        return nodes
    
    # Check if the node is a valid node in range and also checks the surname of the node to ensure it isn't already included in the nodes list
    elif withinRange( getValue(splitnode, enable) , [(p1, p2)], 1) and splitnode.surname not in unique_sur:
        nodes.append(splitnode.point)
        unique_sur.append(splitnode.surname)

    nodes += SearchRangeTree1d(root.left, p1, p2, enable)          # Searching for nodes in left subtree
    nodes += SearchRangeTree1d(root.right, p1, p2, enable)         # Searching for nodes in right subtree
    
    return nodes

    

#print(SearchRangeTree1d(range_tree, 2, 4 , False))


def SearchRangeTree2d (root, x1, x2, y1, y2):
    '''
    Performs 2D range search
    Arguments:
        root        : A Node in tree
        x1          : Starting range for x-coord
        x2          : Ending range for x-coord
        y1          : Starting range for y-coord
        y2          : Ending range for y-coord
    '''

    results = []
    splitnode = FindSplitNode(root, x1, x2, True)

    
    if (splitnode == None):
        return results
    elif withinRange(splitnode.point, [(x1, x2), (y1, y2)], 2) :
        results.append(splitnode.point)
      
    vl = splitnode.left                                                                  # Traverse the nodes in left child of split node
    while ( vl != None ):
        if withinRange(vl.point, [(x1, x2), (y1, y2)], 2):                               # Check if the node is a valid node in range
            results.append(vl.point)

        if (x1 <= vl.point[0]):                                                          # Search the associated tree at the right child of current node 
            if vl.right != None:
                results += SearchRangeTree1d(vl.right.assoc, y1, y2, False)
            vl = vl.left
        else:
            vl = vl.right

    vr = splitnode.right                                                                 # Traverse the nodes in right child of split node
    while ( vr != None ):
        if withinRange(vr.point, [(x1, x2), (y1, y2)], 2):                               # Check if the node is a valid node in range
                results.append(vr.point)
       
        if ( x2 >= vr.point[0] ):                                                        # Search the associated tree at the left child of current node 
            if vr.left != None:
                results += SearchRangeTree1d(vr.left.assoc, y1, y2, False)
            vr = vr.right
        else:
            vr = vr.left
        
    return results

start = time.time()
print(SearchRangeTree2d (range_tree, 65, 82, 2, 12))
end = time.time()

print("Seconds need: ",  end-start)
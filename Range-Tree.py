import csv

#LOAD DATA FROM CSV FILE
#THE DATABASE FEATURES THE SURNAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 
def open_csv_file(surnames, awards, first_letter):
    with open("kdtree_example_set.csv", 'r') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            surnames.append(row[0])
            awards.append(row[1])
    
    for x in range(len(surnames)):
        first_letter.append(ord(surnames[x][0]))    # ord() returns the Unicode code from a given character
    return 


#NODE CLASS  
class Node:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None
        self.isLeaf = False
        self.assoc = None


#RANGE TREE CLASS
class Range_Tree:
    def __init__(self, root: Node = None):
        self.root = root


    #BUILDING 1D RANGE TREE
    def build_range_tree(self, y_nodelist):
        if not y_nodelist:
            return None
           
        mid_val = len(y_nodelist)//2
        new_root = Node(y_nodelist[mid_val].point)
        
        new_root.left = self.build_range_tree(y_nodelist[:mid_val])

        new_root.right = self.build_range_tree(y_nodelist[mid_val+1:])
            
        return new_root


    #BUILDING 2D RANGE TREE
    def build_range_tree2D(self, node_list):
        if not node_list:
            return None
        
        mid_val = len(node_list)//2
        node = node_list[mid_val]  
        if len(node_list)==1:
            node.isLeaf = True

        node.assoc = self.build_range_tree(sorted(node_list, key=lambda node:node.point[1]))       # a bst for every node ordered by y-coordinates
        
        node.left = self.build_range_tree2D(node_list[:mid_val])
        
        node.right = self.build_range_tree2D(node_list[mid_val+1:])
        return node
    

    #PRINTING FUNCTION 
    def print_range_tree(self, root, n=0):
        if root is None:
            return
        
        print(n,". Point is:", root.point, root.isLeaf)
        if root.left != None:
            print(n,". Left Subtree")
            self.print_range_tree(root.left,n+1)
        if root.right != None:
            print(n,". Right Subtree")
            self.print_range_tree(root.right, n+1)

    # 1D RANGE SEARCH FUNCTION
    def withinRange(self, point, range , check):
        """
        Checks if the value of node is within the required range
        Arguments:
            point       : A point in tree
            range       : A list containing range to be checked with
            check       : specifies which option should be performed
        Returns :
            True if in range else False
        """
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
            
    
    def getValue (self, node, enable):
        """
        Reads the desired value from node
        Arguments:
            point       : A point in tree
            enable      : True when we need to read first coord of point when used as a helper function by 2D range search
        """
        if enable:
            value = node.point[0]
        else:
            value = node.point[1]
        return value


    def FindSplitNode(self, root, p_min , p_max, enable):

        '''
        Searches for a common node that splits the range
        Arguments:
            root        : The tree's root
            p_min       : Starting range 
            p_max       : Ending range 
            enable      : True when we need to read first coord of point when used as a helper function by 2D range search
        Returns : A Node
        '''

        splitnode = root
        while splitnode != None:
            node = self.getValue(splitnode, enable)
            if p_max < node:
                    splitnode = splitnode.left
            elif p_min > node:
                    splitnode = splitnode.right
            elif p_min <= node <= p_max:
                    break
        return splitnode
    

    def SearchRangeTree1d (self, root, p1, p2, enable = True):
        '''
        Performs 1D range search
        Arguments:
            root        : A Node in tree
            p1          : Starting range 
            p2          : Ending range 
            enable      : True when we need to read first coord of point when used as a helper function by 2D range search
        '''
        nodes = []
        splitnode = self.FindSplitNode(root , p1, p2, enable)                  # Find the node which the least common ancestor in the tree for given range
        
        if splitnode == None:
            return nodes
        
        # Check if the node is a valid node in range and also checks the surname of the node to ensure it isn't already included in the nodes list
        elif self.withinRange( self.getValue(splitnode, enable) , [(p1, p2)], 1):
            nodes.append(splitnode.point)

        nodes += self.SearchRangeTree1d(splitnode.left, p1, p2, enable)          # Searching for nodes in left subtree
        
        nodes += self.SearchRangeTree1d(splitnode.right, p1, p2, enable)         # Searching for nodes in right subtree
        
        return nodes


    def SearchRangeTree2d (self, root, x1, x2, y1, y2):
            """
            Performs 2D range search
            Arguments:
                root        : A Node in tree
                x1          : Starting range for x-coord
                x2          : Ending range for x-coord
                y1          : Starting range for y-coord
                y2          : Ending range for y-coord
            """
            nodes = []
            splitnode = self.FindSplitNode(root, x1, x2, True)

            
            if (splitnode == None):
                return nodes
            elif self.withinRange(splitnode.point, [(x1, x2), (y1, y2)], 2) :
                nodes.append(splitnode.point)
            
            vl = splitnode.left                                                                # Traverse the nodes in left child of split node
            while ( vl != None ):
                if self.withinRange(vl.point, [(x1, x2), (y1, y2)], 2):                        # Check if the node is a valid node in range
                    nodes.append(vl.point)

                if (x1 <= vl.point[0]):                                                        # Search the associated y-tree at the right child of current node 
                    if vl.right != None:
                        nodes += self.SearchRangeTree1d(vl.right.assoc, y1, y2, False)
                    vl = vl.left
                else:
                    vl = vl.right

            vr = splitnode.right                                                                 # Traverse the nodes in right child of split node
            while ( vr != None ):
                if self.withinRange(vr.point, [(x1, x2), (y1, y2)], 2):                          # Check if the node is a valid node in range
                        nodes.append(vr.point)
            
                if ( x2 >= vr.point[0] ):                                                        # Search the associated tree at the left child of current node 
                    if vr.left != None:
                        nodes += self.SearchRangeTree1d(vr.left.assoc, y1, y2, False)
                    vr = vr.right
                else:
                    vr = vr.left
                
            return nodes


if __name__ == "__main__":
    surnames = []
    awards = []
    first_letter = []                               # The first_letter list holds the first letter of each computer scientist's surname

    open_csv_file(surnames, awards, first_letter)
    awards = [eval(i) for i in awards]              # eval() parses the expression passed to this method and runs python expression within the program
    award_max=max(awards)
   
    data = list(zip(first_letter,awards))           # Combine the first_letter and awards lists

    nodeList = []
    for x in range(len(data)):
        new_node=Node(data[x])
        nodeList.append(new_node)

    nodeList.sort(key= lambda node: node.point)

    
    range_tree = Range_Tree()
    range_tree.root = range_tree.build_range_tree2D(nodeList)         # a bst ordered by x-coordinates

    #range_tree.print_range_tree(range_tree.root.assoc)                # can be used to print either the x-tree or the associated y-trees

    #print(range_tree.SearchRangeTree1d(range_tree.root, 65, 70))

    print(range_tree.SearchRangeTree2d(range_tree.root, 65, 82, 2, 3))

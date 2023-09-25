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

        if len(y_nodelist)==1:
            new_root.isLeaf = True
        
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
            node.assoc = None

        else:
            node.assoc = self.build_range_tree(sorted(node_list, key=lambda node:node.point[1]))       # a bst for every node ordered by y-coordinates
            node.left = self.build_range_tree2D(node_list[:mid_val])
            node.right = self.build_range_tree2D(node_list[mid_val+1:])

        return node
    

    #PRINTING FUNCTION 
    def print_range_tree(self, root, n=1):
        if root is None:
            return
        
        print("The node's point is:", root.point)
        if root.left != None:
            print("Left Child",n)
            self.print_range_tree(root.left,n+1)
        if root.right != None:
            print("Right Child",n)
            self.print_range_tree(root.right, n+1)

    # 1D RANGE SEARCH FUNCTION
    def withinRange(self, point, range , check):

        """
        Checks if the value of node is within the required range
        Arguments:
            point       : A point in tree
            range       : A two dimensional list containing the range to be checked
            check       : specifies whether it's a one or two dimensional value check
        Returns :
            True if in range else False
        """

        if check == 1:
            x = point
            return (x >= range[0][0]  and x <= range[0][1] ) 
            
        elif check == 2:
            x = point[0]
            y = point[1]

            return (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) 
            
            
    
    def getValue (self, node, enable):

        """
        Reads the desired value from node
        Arguments:
            point       : A point in tree
            enable      : True when we need to check the x-coordinate, False when we check the y-coordinate
        """

        if enable:
            value = node.point[0]
        else:
            value = node.point[1]
        return value


    def FindSplitNode(self, root, p_min , p_max, enable):

        '''
        Returns the splitnode where the paths to p_min and p_max split
        Arguments:
            root        : The tree's root
            p_min       : Minimum value 
            p_max       : Maximum value 
            enable      : True when we need to check the x-coordinate, False when we check the y-coordinate
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
            p1          : Minimum value for coordinate
            p2          : Maximum value for coordinate
            enable      : True when we need to check the x-coordinate, False when we check the y-coordinate
        '''

        nodes = []
        splitnode = self.FindSplitNode(root , p1, p2, enable)                 
        
        if splitnode == None:
            return nodes
        
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
                x1          : Minimum value for x-coord
                x2          : Maximum value for x-coord
                y1          : Minimum value for y-coord
                y2          : Maximum value for y-coord
            """

            nodes = []
            splitnode = self.FindSplitNode(root, x1, x2, True)

            
            if (splitnode == None):
                return nodes
            elif self.withinRange(splitnode.point, [(x1, x2), (y1, y2)], 2) :
                nodes.append(splitnode.point)
            
            vl = splitnode.left                                                          # Traverse the nodes in the left subtree of the split node
            while ( vl != None ):
                if self.withinRange(vl.point, [(x1, x2), (y1, y2)], 2):                  # Check if the node is a valid node in range
                    nodes.append(vl.point)

                if (x1 <= vl.point[0]):                                                  # Search the right child's associated y-tree  
                    if vl.right != None:
                        nodes += self.SearchRangeTree1d(vl.right.assoc, y1, y2, False)
                    vl = vl.left
                else:
                    vl = vl.right

            vr = splitnode.right                                                         # Traverse the nodes in right child of split node
            while ( vr != None ):
                if self.withinRange(vr.point, [(x1, x2), (y1, y2)], 2):                  # Check if the node is a valid node in range
                        nodes.append(vr.point)
            
                if ( x2 >= vr.point[0] ):                                                # Search the left child's associated y-tree  
                    if vr.left != None:
                        nodes += self.SearchRangeTree1d(vr.left.assoc, y1, y2, False)
                    vr = vr.right
                else:
                    vr = vr.left
                
            return nodes

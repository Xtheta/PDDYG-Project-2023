#NODE CLASS  
class Node:
    def __init__(self, point):
        self.point = point
        self.index = None 
        self.left = None
        self.right = None
        self.isLeaf = False


#KD TREE CLASS
class KD_Tree:
    def _init_(self, root: Node):
        self.root = root


    #BUILDING 2D KD TREE
    def build_kdtree(self, node_list, depth=0):
        n = len(node_list)
        
        if n <= 0:                                                               # empty set
            return None
        
        axis = depth % 2                                                         # Calculating current axis of comparison
        sorted_list = []
        sorted_list = sorted(node_list, key=lambda node: node.point[axis])       # Sorting nodes by axis-value of each point

        node = sorted_list[n//2]                                                 # The spliting point will be the median

        if n == 1:                                                               # We stop spliting when we reach a leaf node
            node.isLeaf = True
        else:
            node.left = self.build_kdtree(sorted_list[:n // 2], depth+1)
            node.right = self.build_kdtree(sorted_list[n // 2 + 1:], depth+1)

        return node


    #PRINTING FUNCTION
    def print_kdtree(self, root, n=1):
        if root is None:
            return
        
        print("The node's point is:", root.point)
        if root.left != None:
            print("Left Child",n)
            self.print_kdtree(root.left,n+1)
        if root.right != None:
            print("Right Child",n)
            self.print_kdtree(root.right, n+1)


    # 1D RANGE SEARCH FUNCTION
    def withinRange(self, point, range):
        """"
        Checks if the value of the node is within the required range
        Arguments:
            point       : A point in the tree
            range       : A two dimensional list containing range of numbers to be checked
        """

        x = point[0]
        y = point[1]

        return x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] 
            

    # 2D RANGE SEARCH FUNCTION 
    def SearchKDTree2d (self, root, x1, x2, y1, y2, depth=0):
        '''
        Performs 2D range search
        Arguments:
            root        : The tree's root
            x1          : Minimum value for x-coord
            x2          : Maximum value for x-coord
            y1          : Minimum value for y-coord
            y2          : Maximum value for y-coord
        '''
        nodes = []

        if root == None:
            return nodes
        elif self.withinRange(root.point, [(x1, x2), (y1, y2)]) :     # Check if the node is a valid node in range
            nodes.append(root.index)
        
        axis = depth % 2

        if root.point[0]>x2 and axis == 0 :
            nodes += self.SearchKDTree2d(root.left, x1, x2, y1, y2, 1)              # Search for nodes in left subtree
            return nodes
        elif root.point[0]<x1 and axis == 0 :                                       # Search for nodes in right subtree
            nodes += self.SearchKDTree2d(root.right, x1, x2, y1, y2, 1)
            return nodes
        elif root.point[1]>y2 and axis == 1 :                                       # Search for nodes in left subtree
            nodes += self.SearchKDTree2d(root.left, x1, x2, y1, y2, 0)
            return nodes
        elif root.point[1]<y1 and axis == 1 :                                       # Search for nodes in right subtree
            nodes += self.SearchKDTree2d(root.right, x1, x2, y1, y2, 0)             
            return nodes
        else:
            nodes += self.SearchKDTree2d(root.left, x1, x2, y1, y2, depth+1)        # Search for nodes in both subtrees
            nodes += self.SearchKDTree2d(root.right, x1, x2, y1, y2, depth+1)        
            
            return nodes 

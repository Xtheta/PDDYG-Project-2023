import pandas as pd


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
        if n <= 0:
            return None
        
        axis = depth % 2                                                         # Calculating current axis of comparison
        sorted_list = []
        sorted_list = sorted(node_list, key=lambda node: node.point[axis])       # Sorting nodes by axis-value of each point

        node = sorted_list[n//2]                                                 # The spliting point will be the median 
        if n == 1:
            node.isLeaf = True
        node.left = self.build_kdtree(sorted_list[:n // 2], depth+1)
        node.right = self.build_kdtree(sorted_list[n // 2 + 1:], depth+1)

        return node


    #PRINTING FUNCTION
    def print_kdtree(self, root, n=0):
        if root is None:
            return
        
        print(n,". Point is:", root.point, root.isLeaf)
        if root.left != None:
            print(n,". Left Subtree")
            self.print_kdtree(root.left,n+1)
        if root.right != None:
            print(n,". Right Subtree")
            self.print_kdtree(root.right, n+1)


    # 1D RANGE SEARCH FUNCTION
    def withinRange(self, point, range, check):
        """"
        Checks if the value of node is within the required range
        Arguments:
            point       : A point in tree
            range       : A list containing range to be checked with
            check       : specifies which option should be performed
        """
        # 1 DIMENSION
        if check == 1:
            x = point
            return x >= range[0][0]  and x <= range[0][1] 

            
        # 2 DIMENSIONS
        elif check == 2:
            x = point[0]
            y = point[1]

            return x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] 
            

    # 2D RANGE SEARCH FUNCTION 
    def SearchKDTree2d (self, root, x1, x2, y1, y2):
        '''
        Performs 2D range search
        Arguments:
            root        : The tree's root
            x1          : Starting range for x-coord
            x2          : Ending range for x-coord
            y1          : Starting range for y-coord
            y2          : Ending range for y-coord
        '''
        nodes = []

        if root == None:
            return nodes
        elif self.withinRange(root.point, [(x1, x2), (y1, y2)], 2) :     # Check if the node is a valid node in range
            nodes.append(root.index)

        nodes += self.SearchKDTree2d(root.left, x1, x2, y1, y2)          # Search for nodes in left subtree
        nodes += self.SearchKDTree2d(root.right, x1, x2, y1, y2)         # Search for nodes in right subtree
            
        return nodes


if __name__ == "__main__":
    
    #LOAD DATA FROM CSV FILE
    #THE DATABASE FEATURES THE NAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 

    awards = []
    surname_init = []                                            # The first_letter list holds the first letter of each computer scientist's surname

    df = pd.read_csv("scientists.csv", sep=",", header=0)

    for x in range(len(df)):
        words = df['Names'].iloc[x].split()                      # the surname is the last word of the string
        surname_init.append(ord(words[-1][0]))                   # ord() returns the Unicode code from a given character
        awards.append(df['Awards'].iloc[x])

    award_max=max(awards)

    data = list(zip(surname_init,awards))                        # Combine the surname_init and awards lists
    
    nodeList = []
    for x in range(len(data)):
        new_node=Node(data[x])
        new_node.index = x
        nodeList.append(new_node)
    nodeList.sort(key=lambda node: node.point)

    #for x in range(len(nodeList)):
    #   print(nodeList[x].point, nodeList[x].index)
    
    kd_tree = KD_Tree()
    kd_tree.root = kd_tree.build_kdtree(nodeList)

    #kd_tree.print_kdtree(kd_tree.root)

    result = kd_tree.SearchKDTree2d(kd_tree.root, 70, 71, 2, 3)         # a list of indeces
    print(df.iloc[result])
    




    


             
    
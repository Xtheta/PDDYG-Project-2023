import csv


#LOAD DATA FROM CSV FILE
#THE DATABASE FEATURES THE NAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 
def open_csv_file(names, awards, surname_init):
    with open("scientists.csv", 'r', encoding='utf-8') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            names.append(row[0])     
            awards.append(row[1])
    
    for x in range(len(names)):
        words = names[x].split()                  # the surname is the last word of the string
        surname_init.append(ord(words[-1][0]))    # ord() returns the Unicode code from a given character
    return 


#NODE CLASS  
class Node:
    def __init__(self, point, name: None):
        self.point = point
        self.name = name
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
            

    def SearchKDTree1d (self, root, p1, p2, dim):
        """
        Performs 1D range search
        Arguments:
            root        : The tree's root
            p1          : Starting range 
            p2          : Ending range 
            dimension   : x-axis or y-axis
        """
        nodes = []   

        if root == None:
            return nodes
        elif self.withinRange(root.point[dim], [(p1, p2)], 1):        # Check if the node is a valid node in range
            nodes.append(root.point)                                  
        
        nodes += self.SearchKDTree1d(root.left, p1, p2, dim)          # Search for nodes in left subtree
        nodes += self.SearchKDTree1d(root.right, p1, p2, dim)         # Search for nodes in right subtree
        #dokimase na valeis to root.point os orio tou diastimatos anazititsis
        return nodes


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
        elif self.withinRange(root.point, [(x1, x2), (y1, y2)], 2) :       # Check if the node is a valid node in range
            nodes.append(root.point)

        nodes += self.SearchKDTree2d(root.left, x1, x2, y1, y2)          # Search for nodes in left subtree
        nodes += self.SearchKDTree2d(root.right, x1, x2, y1, y2)         # Search for nodes in right subtree
            
        return nodes


if __name__ == "__main__":
    names = []
    awards = []
    surname_init = []                               # The first_letter list holds the first letter of each computer scientist's surname


    open_csv_file(names, awards, surname_init)
    awards = [eval(i) for i in awards]              # eval() parses the expression passed to this method and runs python expression within the program
    award_max=max(awards)
   
   # for x in range(len(surnames)):
    #   print(surnames[x])

    
    data = list(zip(surname_init,awards))           # Combine the surname_init and awards lists
    
    nodeList = []
    for x in range(len(data)):
        new_node=Node(data[x], names[x])
        nodeList.append(new_node)
    nodeList.sort(key=lambda node: node.point)

    for x in range(len(nodeList)):
       print(nodeList[x].point, nodeList[x].name)
    
   

    kd_tree = KD_Tree()
    kd_tree.root = kd_tree.build_kdtree(nodeList)

    #kd_tree.print_kdtree(kd_tree.root)

   # print(kd_tree.SearchKDTree1d(kd_tree.root, 65, 70, 0))

    print(kd_tree.SearchKDTree2d(kd_tree.root, 65, 66, 2, 3))
    




    


             
    

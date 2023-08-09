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
    def _init_(self, root: Node = None):
        self.root = root

    def isroot(self):
        return self.root

    #BUILDING 1D RANGE TREE
    def build_range_tree(self, node_list, a):
        if not node_list:
            return None
        
        mid_val = len(node_list)//2
        root = node_list[mid_val] 
        a+=1
        #print(root.point, a)
        
        root.left = self.build_range_tree(node_list[:mid_val], a)
        root.right = self.build_range_tree(node_list[mid_val+1:], a)
            
        return root


    #BUILDING 2D RANGE TREE
    def build_range_tree2(self, node_list):
        if not node_list:
            return None
        
        mid_val = len(node_list)//2
        node = node_list[mid_val]  
        if len(node_list)==1:
         node.isLeaf = True

        print(self.isroot().point)
        node.left = self.build_range_tree2(node_list[:mid_val])
        print("left")
        print(self.isroot().point)
        node.right = self.build_range_tree2(node_list[mid_val+1:])
        print("right")
        print(self.isroot().point)
        y_nodelist = []
        for i in range(6):
            node = Node((i,i))
            y_nodelist.append(node)
    
        #y_nodelist.sort(key=lambda node: node.point[1])
        node.assoc = self.build_range_tree(y_nodelist, a=0)                     #a bst for every node ordered by y-coordinates
        print("assoc")
        print(self.isroot().point)
        print('\n')
        
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

    nodeList.sort(key=lambda node: node.point)
    
    range_tree = Range_Tree()
    print(range_tree.root)
   # range_tree.root = range_tree.build_range_tree2(nodeList)         # a bst ordered by x-coordinates
    #print(range_tree.root.point)

    range_tree.print_range_tree(range_tree.root)

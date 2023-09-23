import KD_Tree
import Range_Tree
import pandas as pd


#NODE CLASS  
class Node:
    def __init__(self, point):
        self.point = point
        self.index = None 
        self.left = None
        self.right = None
        self.isLeaf = False


if __name__ == "__main__":
    
    #LOAD DATA FROM CSV FILE
    #THE DATABASE FEATURES THE NAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS 
    awards = []
    surname_init = []                                            # The first_letter list holds the first letter of each computer scientist's surname

    df = pd.read_csv("kdtree_example_set.csv", sep=",", header=0)

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

    for x in range(len(nodeList)):
       print(nodeList[x].point, nodeList[x].index)


    menu = {}
    menu['1'] = "Build K-D Tree"
    menu['2'] = "Build Range Tree"
    menu['3'] = "Exit"

    while True:

        print("---------------------")
        print("Menu")
        print("---------------------")
        options=menu.keys()
        for entry in options:
            print (entry, menu[entry])

        selection = input("Please Select:")


        if selection == '1':
            print("---------------------")
            print("K-D Tree")
            kd_tree = KD_Tree.KD_Tree()
            kd_tree.root = kd_tree.build_kdtree(nodeList)


            submenu = {}
            submenu['1'] = "Print K-D Tree"
            submenu['2'] = "Search in K-D Tree"
            submenu['3'] = "Go back"
            opt=submenu.keys()
            for entry in opt:
                print (entry, submenu[entry])
            sel = input("Please Select:")


            if sel == '1':
                kd_tree.print_kdtree(kd_tree.root)

            if sel == '2':
                print("You need to select a range for the search:")
                
                x1 = input("First Letter:")
                x2 = input("Last Letter:")
                x1 = ord(x1.upper())
                x2 = ord(x2.upper())
                y1 = input("Minimum Awards:")
                y2 = input("Maximum Awards:")
                y1 = int(y1)
                y2 = int(y2)

                result = kd_tree.SearchKDTree2d(kd_tree.root, x1, x2, y1, y2)         # a list of indeces
                print(df.iloc[result])

            if sel == '3':
                break
        

        elif selection == '2':
            print("---------------------")
            print("Range Tree")
            range_tree = Range_Tree.Range_Tree()
            range_tree.root = range_tree.build_range_tree2D(nodeList)         # a bst ordered by x-coordinates


            submenu = {}
            submenu['1'] = "Print Range Tree"
            submenu['2'] = "2-D Search in Range Tree"
            submenu['3'] = "Go Back"
            opt=submenu.keys()
            for entry in opt:
                print (entry, submenu[entry])
            sel = input("Please Select:")


            if sel == '1':
                range_tree.print_range_tree(range_tree.root.left.assoc)    # can be used to print either the x-tree or the associated y-trees
           
            if sel == '2':
                print("You need to select a range for the search:")
                
                x1 = input("First Letter:")
                x2 = input("Last Letter:")
                x1 = ord(x1.upper())
                x2 = ord(x2.upper())
                y1 = input("Minimum Awards:")
                y2 = input("Maximum Awards:")
                y1 = int(y1)
                y2 = int(y2)

                nodes = range_tree.SearchRangeTree2d(range_tree.root, x1, x2, y1, y2)     # a list of nodes
                #print(nodes)
                result = []
                for x in range(len(nodeList)):
                   if nodeList[x].point in nodes:
                    result.append(nodeList[x].index)                                    # a list of indices
    
                print(df.iloc[result])

            if sel == '3':
                break

        elif selection == '3':
                break
        
        else: 
            print("Unknown option selected!")
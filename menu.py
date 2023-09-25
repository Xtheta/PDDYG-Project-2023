import KD_Tree
import Range_Tree
import lsh
from pathlib import Path
from timeit import default_timer as timer
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

    df = pd.read_csv("scientists2.csv", sep=",", header=0)

    for x in range(len(df)):
        words = df['Name'].iloc[x].split()                      # the surname is the last word of the string
        surname_init.append(ord(words[-1][0]))                   # ord() returns the Unicode code from a given character
        awards.append(df['Number'].iloc[x])

    award_max=max(awards)



    #for x in range(len(nodeList)):
    #   print(nodeList[x].point, nodeList[x].index)


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
            data = list(zip(surname_init,awards))                        # Combine the surname_init and awards lists
            nodeList = []
            for x in range(len(data)):
                new_node=Node(data[x])
                new_node.index = x
                nodeList.append(new_node)
            nodeList.sort(key=lambda node: node.point)
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

                start = timer()
                result = kd_tree.SearchKDTree2d(kd_tree.root, x1, x2, y1, y2)         # a list of indeces
                end = timer()
                print(end - start, "seconds") # Time in seconds                     

                print(df.iloc[result])

                # LSH 
                # df2 = df.iloc[result]
                # list = df2['Education'].values.tolist()
                # file2 = Path("list.txt")
                # file2.touch(exist_ok=True)
                # file = open(file2, 'w', encoding="utf-8")
                # for row in list:
                #     file.write(f"{row} \n")
                # file.close()
                # res = lsh.main(list)
                # print(lsh.bands, lsh.kShingle, lsh.permutations, lsh.bands, lsh.minPer, lsh.maxPer)
                
                
                # numName = input("Enter the number of file: ")
                # fileResults = "results"+numName+".txt"
                # file1 = Path(fileResults)
                # file1.touch(exist_ok=True)
                # file = open(file1, 'w')
                
                # file.write("Number of k-shingle: " + str(lsh.kShingle) +"\n")
                # file.write("Number of permutations: " + str(lsh.permutations) + "\n")
                # file.write("Number of bands: " + str(lsh.bands) + "\n")
                # file.write("Function for buckets: " + lsh.bucketsVar + "\n")
                # file.write("Minimum percentage: " + str(lsh.minPer) + "%\n")
                # if(lsh.maxPer<lsh.minPer):
                #     lsh.maxPer=100
                # file.write("Maximum percentage: " + str(lsh.maxPer) + "%\n\n\n")
                            
                # for i in range(len(res)):
                #     tempdf = df2.iloc[int(res[i][0])]
                #     templist = tempdf.values.tolist()
                #     file.write(f"Name:{templist[0]} Number:{templist[1]} Education:{templist[2]}\n")
                #     tempdf = df2.iloc[int(res[i][1])]
                #     templist = tempdf.values.tolist()
                #     file.write(f"Name:{templist[0]} Number:{templist[1]} Education:{templist[2]}\n")
                #     file.write(f"percentage: {res[i][2]}%\n\n")
                # file.close()


            if sel == '3':
                break
        

        elif selection == '2':
            print("---------------------")
            print("Range Tree")
            data = list(zip(surname_init,awards))                        # Combine the surname_init and awards lists
            nodeList = []
            for x in range(len(data)):
                new_node=Node(data[x])
                new_node.index = x
                nodeList.append(new_node)
            nodeList.sort(key=lambda node: node.point)
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
                range_tree.print_range_tree(range_tree.root)    # can be used to print either the x-tree or the associated y-trees
           
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

                start = timer()
                nodes = range_tree.SearchRangeTree2d(range_tree.root, x1, x2, y1, y2)     # a list of nodes
                end = timer()
                print(end - start, "seconds") # Time in seconds  


                print(nodes)
                result = []
                for x in range(len(nodeList)):
                   if nodeList[x].point in nodes:
                    result.append(nodeList[x].index)                                    # a list of indices
    
                print(df.iloc[result])

                # LSH 
                # df2 = df.iloc[result]
                # list = df2['Education'].values.tolist()
                # file2 = Path("list.txt")
                # file2.touch(exist_ok=True)
                # file = open(file2, 'w', encoding="utf-8")
                # for row in list:
                #     file.write(f"{row} \n")
                # file.close()
                # res = lsh.main(list)
                # print(lsh.bands, lsh.kShingle, lsh.permutations, lsh.bands, lsh.minPer, lsh.maxPer)
                
                
                # numName = input("Enter the number of file: ")
                # fileResults = "results"+numName+".txt"
                # file1 = Path(fileResults)
                # file1.touch(exist_ok=True)
                # file = open(file1, 'w')
                
                # file.write("Number of k-shingle: " + str(lsh.kShingle) +"\n")
                # file.write("Number of permutations: " + str(lsh.permutations) + "\n")
                # file.write("Number of bands: " + str(lsh.bands) + "\n")
                # file.write("Function for buckets: " + lsh.bucketsVar + "\n")
                # file.write("Minimum percentage: " + str(lsh.minPer) + "%\n")
                # if(lsh.maxPer<lsh.minPer):
                #     lsh.maxPer=100
                # file.write("Maximum percentage: " + str(lsh.maxPer) + "%\n\n\n")
                            
                # for i in range(len(res)):
                #     tempdf = df2.iloc[int(res[i][0])]
                #     templist = tempdf.values.tolist()
                #     file.write(f"Name:{templist[0]} Number:{templist[1]} Education:{templist[2]}\n")
                #     tempdf = df2.iloc[int(res[i][1])]
                #     templist = tempdf.values.tolist()
                #     file.write(f"Name:{templist[0]} Number:{templist[1]} Education:{templist[2]}\n")
                #     file.write(f"percentage: {res[i][2]}%\n\n")
                # file.close()
                

            if sel == '3':
                break

        elif selection == '3':
                break
        
        else: 
            print("Unknown option selected!")

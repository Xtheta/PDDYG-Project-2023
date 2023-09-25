import KD_Tree
import Range_Tree
import Quad_Tree
import R_Tree
import lsh
from pathlib import Path
from timeit import default_timer as timer
import pandas as pd
import os.path
import webScaper
def runLSH(data):

    res = lsh.main(data)

    fileResults = "results"+numName+".txt"
    file1 = Path(fileResults)
    file1.touch(exist_ok=True)
    file = open(file1, 'w')

    file.write("Name of tree: " + nameTree +"\n")
    if(nameTree == "R Tree"):
        file.write("Minimum entries: " + str(m) + "\n")
        file.write("Maximum entries: " + str(M) + "\n")
    file.write("First letter: " + str(x1) + "\n")
    file.write("Last letter: " + str(x2) + "\n")
    file.write("Minimum awards: " + str(y1) + "\n")
    file.write("Maximum awards: " + str(y2) + "\n")
    file.write("Elapsed time for search: " + str(elapsedTime) + " sec\n")
    file.write("Number of k-shingle: " + str(lsh.kShingle) +"\n")
    file.write("Number of permutations: " + str(lsh.permutations) + "\n")
    file.write("Number of bands: " + str(lsh.bands) + "\n")
    file.write("Function for buckets: " + lsh.bucketsVar + "\n")
    file.write("Minimum percentage: " + str(lsh.minPer) + "%\n")
    if(lsh.maxPer<lsh.minPer):
        lsh.maxPer=100
    file.write("Maximum percentage: " + str(lsh.maxPer) + "%\n")
    file.write("Number of similar educations: " + str(len(res))+ "\n\n\n")

    for i in range(len(res)):
        tempdf = df2.iloc[int(res[i][0])]
        templist = tempdf.values.tolist()
        file.write(f"Name: {templist[0]} | Number: {templist[1]} | Education: {templist[2]}\n")
        tempdf = df2.iloc[int(res[i][1])]
        templist = tempdf.values.tolist()
        file.write(f"Name: {templist[0]} | Number: {templist[1]} | Education: {templist[2]}\n")
        file.write(f"percentage: {res[i][2]}%\n\n")
    file.close()
    exit(0)


if __name__ == "__main__":
    checkCSV = os.path.isfile('scientists.csv')
    if(not checkCSV):
        webScaper.main()

    # LOAD DATA FROM CSV FILE
    # THE DATABASE FEATURES THE NAMES, AWARDS AND EDUCATION OF SEVERAL COMPUTER SCIENTISTS
    awards = []
    surname_init = []  # The first_letter list holds the first letter of each computer scientist's surname

    df = pd.read_csv("scientists.csv", sep=",", header=0)

    for x in range(len(df)):
        words = df['Name'].iloc[x].split()  # the surname is the last word of the string
        surname_init.append(ord(words[-1][0]))  # ord() returns the Unicode code from a given character
        awards.append(df['Number'].iloc[x])

    award_max = max(awards)

    # for x in range(len(nodeList)):
    #   print(nodeList[x].point, nodeList[x].index)
    global x1,x2,y1,y2,elapsedTime,nameTree, m, M,numName
    menu = {}
    menu['1'] = "Build K-D Tree"
    menu['2'] = "Build Range Tree"
    menu['3'] = "Build Quad Tree"
    menu['4'] = "Build R Tree"
    menu['5'] = "Break"

    while True:

        print("---------------------")
        print("Menu")
        print("---------------------")
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        selection = input("Please Select:")

        if selection == '1':
            print("---------------------")
            print("K-D Tree")
            data = list(zip(surname_init, awards))  # Combine the surname_init and awards lists
            nodeList = []
            for x in range(len(data)):
                new_node = KD_Tree.Node(data[x])
                new_node.index = x
                nodeList.append(new_node)
            nodeList.sort(key=lambda node: node.point)
            kd_tree = KD_Tree.KD_Tree()
            kd_tree.root = kd_tree.build_kdtree(nodeList)
            print("---------------------")

            submenu = {}
            submenu['1'] = "Print K-D Tree"
            submenu['2'] = "Search in K-D Tree"
            opt = submenu.keys()
            for entry in opt:
                print(entry, submenu[entry])
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
                result = kd_tree.SearchKDTree2d(kd_tree.root, x1, x2, y1, y2)  # a list of indeces
                end = timer()
                elapsedTime = end-start
                # print(end - start, "seconds")  # Time in seconds

                df2 = df.iloc[result]
                list2 = df2.values.tolist()
                list = df2['Education'].values.tolist()

                numName = input("Enter the number of file: ")
                listResults = "list" + numName + ".txt"
                file2 = Path(listResults)
                file2.touch(exist_ok=True)
                file = open(file2, 'w', encoding="utf-8")


                for row in list:
                    file.write(f"{row} \n")
                file.close()
                listAllResilts = "listAll" + numName + ".txt"
                file3 = Path(listAllResilts)
                file3.touch(exist_ok=True)
                file = open(file3, 'w', encoding="utf-8")

                for row in list2:
                    file.write(f"{row} \n")
                file.close()

                nameTree = "K-D Tree"
                runLSH(list)

        elif selection == '2':
            print("---------------------")
            print("Range Tree")
            data = list(zip(surname_init, awards))  # Combine the surname_init and awards lists
            nodeList = []
            for x in range(len(data)):
                new_node = Range_Tree.Node(data[x])
                new_node.index = x
                nodeList.append(new_node)
            nodeList.sort(key=lambda node: node.point)
            range_tree = Range_Tree.Range_Tree()
            range_tree.root = range_tree.build_range_tree2D(nodeList)  # a bst ordered by x-coordinates
            print("---------------------")
            submenu = {}
            submenu['1'] = "Print Range Tree"
            submenu['2'] = "2-D Search in Range Tree"
            opt = submenu.keys()
            for entry in opt:
                print(entry, submenu[entry])
            sel = input("Please Select:")

            if sel == '1':
                range_tree.print_range_tree(
                    range_tree.root)  # can be used to print either the x-tree or the associated y-trees

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
                nodes = range_tree.SearchRangeTree2d(range_tree.root, x1, x2, y1, y2)  # a list of nodes
                end = timer()
                # print(end - start, "seconds")  # Time in seconds

                #print(nodes)
                result = []
                for x in range(len(nodeList)):
                    if nodeList[x].point in nodes:
                        result.append(nodeList[x].index)  # a list of indices

                df2 = df.iloc[result]
                list2 = df2.values.tolist()
                list = df2['Education'].values.tolist()

                numName = input("Enter the number of file: ")
                listResults = "list" + numName + ".txt"
                file2 = Path(listResults)
                file2.touch(exist_ok=True)
                file = open(file2, 'w', encoding="utf-8")

                for row in list:
                    file.write(f"{row} \n")
                file.close()
                listAllResilts = "listAll" + numName + ".txt"
                file3 = Path(listAllResilts)
                file3.touch(exist_ok=True)
                file = open(file3, 'w', encoding="utf-8")

                for row in list2:
                    file.write(f"{row} \n")
                file.close()


                elapsedTime = end - start
                nameTree = "Range Tree"
                runLSH(list)

        elif selection == '3':
            print("---------------------")
            print("Quad Tree")
            x_max = ord('Z')
            x_min = ord('A')
            y_max = award_max
            y_min = 0
            low_point = Quad_Tree.Point(x_min, y_min)
            high_point = Quad_Tree.Point(x_max, y_max)
            rect = Quad_Tree.Rectangle(low_point, high_point)

            qt = Quad_Tree.QuadTree(rect)
            for i in range(0, len(awards)):
                p = Quad_Tree.Point(surname_init[i], awards[i], i)
                qt.insert(p)
            print("---------------------")
            submenu = {}
            submenu['1'] = "Search Quad Tree"
            opt = submenu.keys()
            for entry in opt:
                print(entry, submenu[entry])
            sel = input("Please Select:")

            if sel == '1':
                print("You need to select a range for the search:")

                x1 = input("First Letter:")
                x2 = input("Last Letter:")
                x1 = ord(x1.upper())
                x2 = ord(x2.upper())
                y1 = input("Minimum Awards:")
                y2 = input("Maximum Awards:")
                y1 = int(y1)
                y2 = int(y2)

                data_rec = Quad_Tree.Rectangle(Quad_Tree.Point(x1, y1), Quad_Tree.Point(x2, y2))
                start = timer()
                result = qt.range_search(qt.root, data_rec)
                end = timer()

                df2 = df.iloc[result]
                list2 = df2.values.tolist()
                list = df2['Education'].values.tolist()

                numName = input("Enter the number of file: ")
                listResults = "list" + numName + ".txt"
                file2 = Path(listResults)
                file2.touch(exist_ok=True)
                file = open(file2, 'w', encoding="utf-8")

                for row in list:
                    file.write(f"{row} \n")
                file.close()
                listAllResilts = "listAll" + numName + ".txt"
                file3 = Path(listAllResilts)
                file3.touch(exist_ok=True)
                file = open(file3, 'w', encoding="utf-8")

                for row in list2:
                    file.write(f"{row} \n")
                file.close()

                elapsedTime = end - start
                nameTree = "Quad Tree"
                runLSH(list)

        elif selection == '4':
            print("---------------------")
            print("R Tree")
            print("---------------------")

            while (1):
                print("Please choose integers minimum and Maximum for your R Tree where m<=M/2")
                m = int(input("Minimum:"))
                M = int(input("Maximum:"))
                if m <= M / 2:
                    break

            r = R_Tree.RTree(M, m)

            for i in range(0, len(awards)):
                data_rec = R_Tree.Rectangle(R_Tree.Point(surname_init[i], awards[i]), R_Tree.Point(surname_init[i], awards[i]))
                r.insertion(data_rec, i)

            print("---------------------")
            submenu = {}
            submenu['1'] = "Search R Tree"
            opt = submenu.keys()
            for entry in opt:
                print(entry, submenu[entry])
            sel = input("Please Select:")

            if sel == '1':
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
                result = r.search_tree(R_Tree.Rectangle(R_Tree.Point(x1, y1), R_Tree.Point(x2, y2)))
                end = timer()

                df2 = df.iloc[result]
                list2 = df2.values.tolist()
                list = df2['Education'].values.tolist()

                numName = input("Enter the number of file: ")
                listResults = "list" + numName + ".txt"
                file2 = Path(listResults)
                file2.touch(exist_ok=True)
                file = open(file2, 'w', encoding="utf-8")

                for row in list:
                    file.write(f"{row} \n")
                file.close()
                listAllResilts = "listAll" + numName + ".txt"
                file3 = Path(listAllResilts)
                file3.touch(exist_ok=True)
                file = open(file3, 'w', encoding="utf-8")

                for row in list2:
                    file.write(f"{row} \n")
                file.close()

                elapsedTime = end - start
                nameTree = "R Tree"
                runLSH(list)

        elif selection == '5':
            exit(0)

        else:
            print("Unknown option selected!")

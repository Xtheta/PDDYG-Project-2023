import csv
from random import shuffle
from math import ceil, log
import numpy as np
from itertools import combinations


exceptions = ['OF', 'AND', 'TO', 'IN', 'AT', 'THE', 'BY', 'FOR', 'NO', 'WHO', 'WAS', 'ONE', 'A']
bucketsVar = ""
def preprocess_text(text):
    tokens = text.upper().split()

    filtered_tokens = [token.lower() for token in tokens if token not in exceptions]
    return ' '.join(filtered_tokens)
def shingling(text, k):
    shingles = []
    for i in range(len(text) - k + 1):
        shingles.append(text[i:i + k].lower())
    return set(shingles)

def crsuffle(length):
    hash_ex = list(range(1, length + 1))
    shuffle(hash_ex)
    return hash_ex

def buildMinhashFunc(perms, length):
    hashes = []
    hash_ex = list(range(1, length + 1))
    hashes.append(hash_ex)
    for i in range(1,perms):
        hashes.append(crsuffle(length))
    return hashes

def creatSignatu(matrix, minhash, data):
    signature = [[] for _ in range(len(data))]

    for i in range(len(minhash)):
        for j in range(len(matrix[i])):
            if(matrix[i][j]):
                if(len(signature[j])==0):
                    signature[j] = minhash[i].copy()
                else:
                    check = signature[j]<=minhash[i]
                    for k in range(0, len(check)):
                        if(not check[k]):
                            signature[j][k] = minhash[i][k]

    return signature

def createBuckets(bands, lenData, splitedSignatures):
    numOfBuckets = ceil(100 * log(lenData))
    global bucketsVar
    bucketsVar = "numOfBuckets = ceil(100 * log(lenData))"
    # numOfBuckets = len(data)
    # numOfBuckets = int(0.75 *len(data))
    totalbucketlist = []
    for band in range(bands):
        band_list = [[] for _ in range(numOfBuckets)]
        for text in range(lenData):
            band_list[abs(hash(tuple(splitedSignatures[text][band]))) % numOfBuckets].append(text)
        totalbucketlist.append(band_list)

    return totalbucketlist

def candidatePairs(totalBuckets):
    pairSet = set()
    for band in totalBuckets:
        for index in range(len(band)):
            for comb in combinations(band[index], 2):
                pairSet.add(comb)

    return pairSet

def similarity(minPercentage, maxPercentage, pairSet, splitedSignatures, data,bands):
    results = []
    for i in pairSet:
        text1 = i[0]
        text2 = i[1]

        sign1 = splitedSignatures[text1]
        sign2 = splitedSignatures[text2]

        count = 0
        for i in range(len(sign1)):
            if(len(sign1[0])!=0):
                if(sign1[i]==sign2[i]):
                    count+=1
            else:
                count = 0
                break


        percentage = round(((count/bands)*100),2)
        if(percentage==100.00):
            if(len(data[text1])==0 and len(data[text2])==0):
                percentage = 0.00

        if(minPercentage<maxPercentage):
            if (percentage >= minPercentage and percentage<=maxPercentage):
                # print(f"\n{text1}: {data[text1]}\n{text2}: {data[text2]}\nPERCENTAGE: ", percentage, "%")
                results.append([f"{text1}: {data[text1]}", f"{text2}: {data[text2]}", f"PERCENTAGE: {percentage}%"])
        else:
            if (percentage >= minPercentage):
                # print(f"\n{text1}: {data[text1]}\n{text2}: {data[text2]}\nPERCENTAGE: ",percentage,"%")
                results.append([f"{text1}: {data[text1]}", f"{text2}: {data[text2]}", f"PERCENTAGE: {percentage}%"])


    return results

def splitSignature(signature, b):
    r = int(len(signature)/b)
    splits = []
    if r != 0:
        for i in range(0, len(signature), r):
            splits.append(signature[i:i+r])
    else:
        for i in range(0, b):
            splits.append([])
    return splits

def main(data):
    numName = input("Enter the number of file: ")
    fileResults = "results"+numName+".txt"
    kShingle = int(input("Enter the number of k-Shingle: "))
    permutations = int(input("Enter the number of permutations: "))
    bands = int(input("Enter the number of bands: "))
    minPer = int(input("Enter minimum percentage of similarity: "))
    maxPer = int(input("Enter maximum percentage of similarity: "))


    # data = []
    # with open('scientists.csv', 'r', encoding='utf-8') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     header = next(csvreader)
    #     for row in csvreader:
    #         data.append(row[2])

    # data = ["haris einai","nikos einai","einai einai"]

    shingledData = set()
    for row in data:
        preprocessed_text = preprocess_text(row)
        shingledData.update(shingling(preprocessed_text, kShingle))

    vocablary = list(shingledData)

    matrix = []
    for shingle in vocablary:
        row = []
        for text in data:
            if shingle in text.lower():
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)

    minhash = buildMinhashFunc(permutations, len(vocablary))
    minhash = np.column_stack(minhash)

    signatures = creatSignatu(matrix,minhash,data)
    splitedSignatures = []

    for signature in signatures:
        signature = list(signature)
        splitedSignatures.append(splitSignature(signature,bands))


    totalbucketlist = createBuckets(bands, len(data), splitedSignatures)


    pairSet = candidatePairs(totalbucketlist)

    res = similarity(minPer,maxPer,pairSet,splitedSignatures,data,bands)

    file = open(fileResults, 'w')

    file.write("Number of k-shingle: " + str(kShingle) +"\n")
    file.write("Number of permutations: " + str(permutations) + "\n")
    file.write("Number of bands: " + str(bands) + "\n")
    file.write("Function for buckets: " + bucketsVar + "\n")
    file.write("Minimum percentage: " + str(minPer) + "%\n")
    if(maxPer<minPer):
        maxPer=100
    file.write("Maximum percentage: " + str(maxPer) + "%\n\n\n")

    for row in res:
        for i in row:
            file.write(i + "\n")
    file.close()

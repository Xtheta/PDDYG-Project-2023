import csv
import itertools
from random import shuffle, random
from math import ceil, sqrt, log

import numpy as np
from tqdm import tqdm
from itertools import combinations


exceptions = ['OF', 'AND', 'TO', 'IN', 'AT', 'THE', 'BY', 'FOR', 'NO', 'WHO', 'WAS', 'ONE', 'A']

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

if __name__ == '__main__':

    data = []
    with open('scientists.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            data.append(row[2])


    shingledData = set()
    for row in data:
        preprocessed_text = preprocess_text(row)
        shingledData.update(shingling(preprocessed_text, 5))

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

    # Create headers for the CSV file
    # headers = [f'text{i}' for i in range(len(data))]
    # headers.insert(0, "Shingles")
    # csv_filename = 'output.csv'
    # # Write the matrix to a CSV file
    # with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(headers)
    #     csvwriter.writerows(matrix)



    permutations = 20
    minhash = buildMinhashFunc(permutations, len(vocablary))
    minhash = np.column_stack(minhash)
    signatures = creatSignatu(matrix,minhash,data)
    splitedSignatures = []
    bands = 5

    for signature in signatures:
        signature = list(signature)
        splitedSignatures.append(splitSignature(signature,bands))


    numOfBuckets = ceil(100 * log(len(signatures)))
    # numOfBuckets = len(data)
    # numOfBuckets = int(0.75 *len(data))
    cnt = 2
    totalbucketlist = []
    for band in range(len(splitedSignatures[0])):
        band_list = [[] for _ in range(numOfBuckets)]
        for text in range(len(signatures)):
            # print(text, abs(hash(tuple(splitedSignatures[text][band]))),abs(hash(tuple(splitedSignatures[text][band])))% len(data))
            band_list[abs(hash(tuple(splitedSignatures[text][band])))%numOfBuckets].append(text)

        totalbucketlist.append(band_list)

    pairSet = set()
    for band in totalbucketlist:
        for index in range(len(band)):
            for comb in combinations(band[index], 2):
                pairSet.add(comb)
        break



    for i in pairSet:
        text1 = i[0]
        text2 = i[1]

        sign1 = splitedSignatures[text1]
        sign2 = splitedSignatures[text2]
        check = 0
        count = 0
        for i in range(len(sign1)):
            if(len(sign1[0])!=0):
                if(sign1[i]==sign2[i]):
                    count+=1
            else:
                count = 0
                break
            check = 1

        percentage = (count/bands)*100

        if(check):
            if(percentage>20 and percentage<100):
                print(f"\n{text1}: {data[text1]}\n{text2}: {data[text2]}\nPERCENTAGE: ",percentage,"%")

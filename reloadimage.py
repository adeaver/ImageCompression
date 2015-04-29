from pickle import load
from math import cos, pi
from compressdct import quality, calcDCT, intoList
from PIL import Image
from numpy import dot, matrix, array
import re

def reverse_quality(quality, dct_matrix):
    new_matrix = []
    for num_row in range(0, 8):
        row_divide = list(array(quality[num_row]).reshape(-1))
        row_dct = list(array(dct_matrix[num_row]).reshape(-1))

        row_final = []

        for element in range(0, 8):
            row_final.append(round(row_dct[element] * row_divide[element]))

        new_matrix.append(row_final)

    return matrix(new_matrix)

def performIDCT(dct, img):
    return dot(dot(dct.transpose(), img), dct) + 128

def roundElements(mat):
    rounded = []

    for base in range(len(mat)):
        row = []
        for x in range(len(mat[base])):
            row.append(int(mat[base][x]))
        rounded.append(row)

    return rounded

def stringToList(string):
    mat = []
    initFormat = re.sub("\[", "", string[1:len(string)-1])
    listFormat = initFormat.split("]")
    
    for newList in listFormat:
        numList = newList.split(", ")
        row = []
        for num in numList:
            if(len(num)>0):
                row.append(float(num))

        if(len(row) > 0):
            mat.append(row)

    return mat

def loadAndUnpack():
    data_packed = load(open("compressed.jvad", "rb"))

    data = []
    mat = []

    for index in range(len(data_packed)):
        line = data_packed[index]
        mat = stringToList(line.decode('utf-8'))
        data.append(mat)

    return data


def uncompress(data):
    quality_matrix = quality(50)
    dct = matrix(calcDCT())

    final_data = []

    for index in range(len(data)):
        data_mat = matrix(data[index])
        reved = reverse_quality(quality_matrix, data_mat)
        newimg = performIDCT(dct, reved)
        imglist = roundElements(intoList(newimg))
        final_data.append(imglist)

        if(index == 0):
            print imglist

uncompress(loadAndUnpack())
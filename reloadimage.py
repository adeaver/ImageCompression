from pickle import load
from math import cos, pi, sqrt
from compressdct import quality, calcDCT, intoList
from PIL import Image
from numpy import dot, matrix, array
import re
from encoding import Decoder

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

def build_mat(y_data, x_data, color_data):
    mat = [[0 for x in range(8)] for y in range(8)]
    
    for num in range(len(y_data)):
        y = y_data[num]
        x = x_data[num]
        color = color_data[num]

        mat[x][y] = color

    return mat

def loadAndUnpack():
    dec = Decoder("compressed.jvad")
    dec.decode_as("uncompressed.jvad")
    data_packed = load(open("uncompressed.jvad", "rb"))

    data = []
    mat = []

    for index in range(len(data_packed)):
        packet = data_packed[index].split(" ")

        y_data = []
        x_data = []
        color_data = []

        for info in packet:
            if(len(info)>0):
                y_data.append(int(info[0], 16))
                x_data.append(int(info[1], 16))
                if(info[len(info)-1] == "n"):
                    color_data.append(int(info[2:len(info)-1], 16) * -1)
                else:
                    color_data.append(int(info[2:], 16))

        mat = build_mat(y_data, x_data, color_data)
        # line = data_packed[index]
        # mat = stringToList(line.decode('utf-8'))
        data.append(mat)

    print mat

    return data


def getData(data):
    quality_matrix = quality(99)
    dct = matrix(calcDCT())

    final_data = []

    for index in range(len(data)):
        data_mat = matrix(data[index])
        reved = reverse_quality(quality_matrix, data_mat)
        newimg = performIDCT(dct, reved)
        imglist = roundElements(intoList(newimg))
        final_data.append(imglist)

    return final_data

def uncompress(data):
    width = 511
    height = 512

    num_x = (width-width%8)
    num_y = (height-height%8)

    im = Image.new("RGB", (width, height))
    pixels = im.load()

    index = -1

    end_range = int(round(sqrt(len(data))))

    print end_range

    for y_step in range(end_range):
        for x_step in range(end_range):
            index += 1
            if(index >= len(data)):
                break
            y_pixel = y_step * 8
            for y in range(8):
                x_pixel = x_step * 8
                for x in range(8):
                    pixels[x_pixel, y_pixel] = (data[index][y][x],
                                                data[index][y][x],
                                                data[index][y][x])
                    x_pixel += 1
                y_pixel += 1

    im.show()

data = getData(loadAndUnpack())
uncompress(data)
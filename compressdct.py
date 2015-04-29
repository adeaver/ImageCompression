from numpy import matrix, array, dot
from math import sqrt, cos, pi
from PIL import Image
from pickle import dump
import array as ar

def getGrayscaleValues(img):
    width = img.size[0]
    height = img.size[0]

    grayscaleValues = []

    # im = Image.new("RGB", (width, height))
    # pixels = im.load()

    for y in range(height):
        grayScaleRow = []
        for x in range(width):
            rgb = img.getpixel((x, y))
            gray = (rgb[0] * .299 + rgb[1] * .587 + rgb[2] * .114)-127
            grayScaleRow.append(int(gray))
            # pixels[x, y] = (int(gray), int(gray), int(gray))
        grayscaleValues.append(grayScaleRow)

    # im.show()

    return grayscaleValues

def quality(quality):
    if(quality >= 50):
        quality = (100-quality)/50.0
    else:
        quality = 50.0/quality

    q_matrix = matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]])

    return q_matrix * quality


def quantize(gValues):
    mat = []
    step = 8
    for y_step in range(0, len(gValues)-(len(gValues)%8), step):
        row = []
        for x_step in range(0, len(gValues[0])-(len(gValues[0])%8), step):
            mini_mat = []
            for y in range(y_step, y_step+step):
                mini_row = []
                for x in range(x_step, x_step+step):
                    mini_row.append(gValues[y][x])
                mini_mat.append(mini_row)
            mat.append(mini_mat)

    return mat

def quality_divide(quality, dct_matrix):
    new_matrix = []
    for num_row in range(0, 8):
        row_divide = list(array(quality[num_row]).reshape(-1))
        row_dct = list(array(dct_matrix[num_row]).reshape(-1))

        row_final = []

        for element in range(0, 8):
            row_final.append(round(row_dct[element]/row_divide[element]))

        new_matrix.append(row_final)

    return matrix(new_matrix)

def performDCT(vals, dct):
    return dot(dot(dct, vals), dct.transpose())

def calcDCT():
    matrix = []
    for y in range(0, 8):
        row = []
        for x in range(0, 8):
            if(y == 0):
                row.append(1/sqrt(8))
            else:
                row.append(sqrt(2/8.0) * cos(((2*x+1)*y * pi)/16.0))
        matrix.append(row)

    return matrix

def intoList(mat):
    final_matrix = []
    for index in range(8):
        row = list(array(mat[index]).reshape(-1))
        final_matrix.append(row)
    return final_matrix

def nonZeros(index, mat):
    entries = []
    for y in range(len(mat)):
        for x in range(len(mat[y])):
            if(mat[y][x] != 0):
                entries += [index, x, y, mat[y][x]]

    return entries

def compress(quantized):
    dct = matrix(calcDCT())
    quality_matrix = quality(99)

    allSquares = []

    for index in range(len(quantized)):
        quantize_matrix = matrix(quantized[index])
        dct_perform = performDCT(quantize_matrix, dct)
        final_dct = quality_divide(quality_matrix, dct_perform)
        square = intoList(final_dct)
        # nonzeros = nonZeros(index, square)
        allSquares.append(bytearray(str(square)))

    dump(allSquares, open("compressed.jvad", "wb"))


file_name = "xxxrobbiexxx.jpg"

img = Image.open(file_name)
# img.show()

gValues = getGrayscaleValues(img)
quantized = quantize(gValues)

# verify = []
# for list1 in quantized[0]:
#     row = []
#     for num in list1:
#         row.append(num+127)
#     verify.append(row)

# print verify

# print len(quantized[0])
compress(quantized)
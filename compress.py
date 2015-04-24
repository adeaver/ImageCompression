from PIL import Image
import matplotlib.pyplot as plt
from math import cos, pi
from numpy import matrix, dot
from pickle import load


def getGrayscaleValues(img):
    width = img.size[0]
    height = img.size[0]

    grayscaleValues = []

    im = Image.new("RGB", (width, height))
    pixels = im.load()

    for y in range(height):
        grayScaleRow = []
        for x in range(width):
            rgb = img.getpixel((x, y))
            gray = rgb[0] * .299 + rgb[1] * .587 + rgb[2] * .114
            grayScaleRow.append(int(gray))
            pixels[x, y] = (int(gray), int(gray), int(gray))
        grayscaleValues.append(grayScaleRow)

    im.show()

    return grayscaleValues

def eightbyeight(gValues):
    mat = []
    step = 5
    for y_step in range(0, len(gValues), step):
        row = []
        for x_step in range(0, len(gValues[0]), step):
            avg_val = 0
            for x in range(x_step, x_step+step):
                for y in range(y_step, y_step+step):
                    avg_val += gValues[y][x]
            row.append(avg_val/64)
        mat.append(row)
    return mat

def coefficients(gValues):
    C_matrix = []
    for l in range(len(gValues)):
        C_row = []
        for k in range(len(gValues[0])):
            I_sum = 0
            for m in range(len(gValues)):
                for n in range(len(gValues[0])):
                    I_sum += gValues[m][n] * cos((pi * (k * n + l * m))/len(gValues))
            C_row.append(I_sum)
        C_matrix.append(C_row)
    return C_matrix

file_name = "file.png"

img = Image.open(file_name)
img.show()

gValues = getGrayscaleValues(img)
avg = eightbyeight(gValues)

im = Image.new("RGB", (len(avg[0]), len(avg)))
pixels = im.load()

for y in range(len(avg)):
    for x in range(len(avg[0])):
        pixels[x, y] = (avg[y][x], avg[y][x], avg[y][x])

im.show()
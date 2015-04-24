from PIL import Image
import matplotlib.pyplot as plt
from math import cos, pi
from numpy import matrix, dot
from pickle import load


def getGrayscaleValues(img):
    width = img.size[0]
    height = img.size[0]

    grayscaleValues = []

    for y in range(height):
        grayScaleRow = []
        for x in range(width):
            rgb = img.getpixel((x, y))
            gray = rgb[0] * .299 + rgb[1] * .587 + rgb[2] * .114
            grayScaleRow.append(int(gray))
        grayscaleValues.append(grayScaleRow)

    return grayscaleValues

file_name = "file.png"

img = Image.open(file_name)
gValues = getGrayscaleValues(img)
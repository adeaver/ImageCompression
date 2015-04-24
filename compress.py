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
        for x in range(width):
            rgb = img.getpixel((x, y))
            gray = rgb[0] * .299 + rgb[1] * .587 + rgb[2] * .114
            grayscaleValues.append(int(gray))

    return grayscaleValues

def getFreq(n, N):
    if(n <= N):
        return [cos((2 * pi * n)/N)] + getFreq(n+1, N)
    else:
        return [cos((2 * pi * n)/N)]

def expMatrix(exp, numlist):
    return [num ** exp for num in numlist]

def readFile(file_name):
    file_split = file_name.split(".")
    openFile = file_split[0] + "_compressed.jvad"

file_name = "file.png"

img = Image.open(file_name)
gValues = getGrayscaleValues(img)
plt.plot(gValues)
plt.ylabel("Grayscale Values")
plt.xlabel("Time")
plt.show()
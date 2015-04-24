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

def getSamples(step, gValues):
    return [gValues[index] for index in range(0, len(gValues), step)]

def getXValues(step, gValues):
    return [index for index in range(0, len(gValues), step)]

def getFreq(n, N, k):
    freqList = []

    for i in range(n, N):
        freqList = cos((2 * pi * i * k)/N)

    return freqList

def expMatrix(exp, numlist):
    return [num ** exp for num in numlist]

def readFile(file_name):
    file_split = file_name.split(".")
    openFile = file_split[0] + "_compressed.jvad"

file_name = "file.png"

img = Image.open(file_name)
gValues = getGrayscaleValues(img)

step = len(gValues)/3000

sampled = getSamples(step, gValues)
xVals = getXValues(step, gValues)

plt.plot(xVals, sampled)
#plt.plot(gValues)
plt.ylabel("Grayscale Values")
plt.xlabel("Time")
plt.show()
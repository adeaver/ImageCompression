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

def getSamples(step, gValues):
    return [gValues[index] for index in range(0, len(gValues), step)]

def getXValues(step, gValues):
    return [index for index in range(0, len(gValues), step)]

def getFreq(n, N, k):
    freqList = []

    for i in range(n, N):
        freqList = cos((pi * i * k)/N)

    return freqList

file_name = "file.png"

img = Image.open(file_name)
gValues = getGrayscaleValues(img)

N = 3000

step = len(gValues)/N

sampled = getSamples(step, gValues)
xVals = getXValues(step, gValues)

plt.plot(xVals, sampled)
#plt.plot(gValues)
plt.ylabel("Grayscale Values")
plt.xlabel("Time")
plt.show()

# allFreqs = []

# for x in range(0, N):
#     allFreqs.append(getFreq(1, N, x))

# freq_matrix = matrix(allFreqs)
# time_matrix = matrix(sampled[:N]).transpose()
# print freq_matrix.shape
# print time_matrix.shape
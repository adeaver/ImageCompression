from pickle import load
from math import cos, pi

def getValues(gValues):
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

data = load(open("compress.jvad", "rb"))

print getValues(data[0])

# for line in data[0]:
#     print line
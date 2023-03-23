from csv import reader
import math
import numpy

# Returns true if value is a perfect square
def checkSquare(length):
    return (math.sqrt(length) * math.sqrt(length)) == length

# Reshape array into matrix of type numpyarray
def convert(matrix):
    print("this matrix:")
    print(matrix)
    nMatrix = numpy.fromstring(matrix, dtype=float, sep=',') 
    newMatrix = numpy.reshape(nMatrix, (int(math.sqrt(len(nMatrix))), int(math.sqrt(len(nMatrix)))))
    return numpy.asarray(newMatrix).astype(float)

# Takes a filename and returns list of all matrices
# Return type is numpy array of integers
def readFile(fileName):
    with open(fileName, 'r') as file:
        csv_reader = reader(file)
        matrices = []
        current = 0
        for matrix in csv_reader:
            current += 1
            validLength = checkSquare(len(matrix))
            if validLength:
                for row in matrix:
                    for value in row:
                        value = float(value)
                longMatrix = convert(matrix)
                matrices.append(numpy.asarray(longMatrix))
            else:
                #Placeholder to throw error
                print("Not valid matrix size on line" + str(current))
        return matrices

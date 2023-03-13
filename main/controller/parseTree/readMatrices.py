from csv import reader
import math
import numpy

# Returns true if value is a perfect square
def checkSquare(length):
    return (math.sqrt(length) * math.sqrt(length)) == length

# Reshape array into matrix
def convert(matrix):
    i = 0
    while i < len(matrix):
        numpy.reshape(matrix, len(matrix))
        i += 1

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
                        value = int(value)
                newMatrix = numpy.reshape(matrix, (int(math.sqrt(len(matrix))), int(math.sqrt(len(matrix)))))
                longMatrix = numpy.asarray(newMatrix).astype(float)
                matrices.append(numpy.asarray(longMatrix))
            else:
                #Placeholder to throw error
                print("Not valid matrix size on line" + str(current))
        return matrices

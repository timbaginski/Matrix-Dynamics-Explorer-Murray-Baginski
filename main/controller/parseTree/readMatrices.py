from csv import reader
import math
import numpy as np
import pandas as pd
import json

# Returns true if value is a perfect square
def checkSquare(length):
    return (math.sqrt(length) * math.sqrt(length)) == length

# Reshape array into matrix of type numpyarray
def convert(matrix):
    print("this matrix:")
    nMatrix = np.fromstring(matrix, dtype=float, sep=',') 
    newMatrix = np.reshape(nMatrix, (int(math.sqrt(len(nMatrix))), int(math.sqrt(len(nMatrix)))))
    return np.asarray(newMatrix).astype(float)

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
                matrices.append(np.asarray(longMatrix))
            else:
                #Placeholder to throw error
                print("Not valid matrix size on line" + str(current))
        return matrices
    
def csvToMatrices(csv):
    matrices = []
    for line in csv.file:
        line_str = line.decode('utf-8')
        line_str = line_str.replace('\r', '')
        line_str = line_str.replace('\n', '')
        line_list = line_str.split(',')  
        matrix = []
        for i in range(0, len(line_list), int(math.sqrt(len(line_list)))):
            temp = []
            for j in range(i, i+int(math.sqrt(len(line_list)))):
                temp.append(line_list[j])

            matrix.append(temp)
        
        matrices.append(json.dumps(matrix))
    
    return matrices



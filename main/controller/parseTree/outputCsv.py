import csv
import math
import numpy

def toCsv(iterations, fileName):
    with open(fileName, 'w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)
        iteration = 0
        
        # Write the data to the file
        for row in iterations:
            iteration += 1
            writer.writerow(row)
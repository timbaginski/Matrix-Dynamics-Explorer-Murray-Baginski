from .parseTree import ParseTree

class maxIteration():

    def __init__(self):
        self.root = None

    # Takes polynomial, max number of iterations, and starting value
    # Returns list of value at each iteration
    def allIterations(self, polynomial, maxVal, startVal):
        i = 0
        results = [0 for x in range(maxVal+1)]
        poly = ParseTree()
        poly.parsePoly(poly=polynomial)
        results[0] = startVal
        while i < maxVal:
            i += 1
            ## showIteration(i, maxVal)
            results[i] = poly.callPoly(results[i-1])
        return results
    
    # Based on results checks to see if threshold is reached
    def diverges(self, results, threshold):
        print(results[len(results)-1] - results[len(results)-2])
        return (results[len(results)-1] - results[len(results)-2]) > threshold
    
    def showIteration(current, end):
        ## Line below is placeholder until we have frontend working
        print(current + "/" + end)

    # Only needed if allIterations doesn't work for matrices, so far it isnt used
    def matrixIterations(self, polynomial, maxVal, startMatrix):
        i = 0
        results = [0 for x in range(maxVal+1)]
        poly = ParseTree()
        poly.parsePoly(poly=polynomial)
        results[0] = startMatrix
        while i < maxVal:
            i += 1
            ## showIteration(i, maxVal)
            results[i] = poly.callPoly(results[i-1])
        return results
    

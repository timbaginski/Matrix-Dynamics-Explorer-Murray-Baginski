from .parseTree import ParseTree
from ...models import Iteration, IterationStep
import json
import numpy as np
from django.core.exceptions import ObjectDoesNotExist

class MaxIteration():

    def __init__(self):
        self.root = None

    # Takes polynomial, max number of iterations, and starting value
    def allIterations(self, iteration):
        res = [iteration.startValue]
        i = 1
        poly = ParseTree()
        poly.parsePoly(poly=iteration.polynomial)

        # insert first iteration step
        startValue = iteration.startValue 
        if startValue.isdigit():
            startValue = int(startValue)
        elif startValue.replace('.','',1).isdigit():
            startValue = float(startValue)
        else:
            print(startValue)
            startValue = list(json.loads(startValue))
            startValue = np.asarray(startValue)
            startValue = startValue.astype('float32')

        value = poly.callPoly(startValue)

        if type(value) == float or type(value) == int:
            first = IterationStep(iterationID=iteration, value=value, step=0)
        else:
            value = value.tolist()
            first = IterationStep(iterationID=iteration, value=json.dumps(value), step=0)
        
        first.save()

        while i < iteration.maxIteration:
            ## showIteration(i, maxVal)
            iteration.currentIteration = i
            iteration.save()
            previousSet = IterationStep.objects.filter(iterationID=iteration.id)
            previous = previousSet.get(step=i-1)
            prevValue = previous.value 

            if prevValue.isdigit():
                prevValue = int(prevValue)
            elif prevValue.replace('.','',1).isdigit():
                prevValue = float(prevValue)
            else:
                prevValue = json.loads(prevValue)
                prevValue = np.asarray(prevValue)

            newValue = poly.callPoly(prevValue)
            if type(newValue) == int or type(newValue) == float:
                newStep = IterationStep(iterationID=iteration, value=str(newValue), step=i)

            else:
                newValue = newValue.tolist()
                newValue = json.dumps(newValue)
                newStep = IterationStep(iterationID=iteration, value=newValue, step=i)
            
            res.append(newStep.value)
            newStep.save()
            i += 1
        
        iteration.currentIteration = i
        iteration.converged = not self.diverges(res, iteration.threshold)
        iteration.save()
    
        return res
    
    # Based on results checks to see if threshold is reached
    def diverges(self, results, threshold):
        if type(results[0]) == str and (results[0].isdigit() or results[0].replace('.','',1).isdigit()):
            return float(results[-1]) - float(results[-2]) > threshold
        # print(results[len(results)-1] - results[len(results)-2])
        if type(results[0] == str):
            results[-1] = json.loads(results[-1])
            results[-2] = json.loads(results[-2])
            results[-1] = np.asarray(results[-1])
            results[-2] = np.asarray(results[-2])


        return abs(np.linalg.norm(results[len(results)-1]) - np.linalg.norm(results[len(results)-2])) > threshold
    
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
    
    # returns the value the matrix converged on given an id
    def getConvergeValue(self, id):
        iteration = Iteration.objects.get(pk=id)

        if iteration == None:
            return None
        
        iterationSteps = IterationStep.objects.filter(iterationID=id)
        try:
            iterationStep = iterationSteps.get(step=iteration.currentIteration - 1)
        except ObjectDoesNotExist:
            return None
        
        return iterationStep.value
    
    # starts the iteration when given an id
    def startIteration(self, id):
        iteration = Iteration.objects.get(pk=id)

        if iteration == None:
            return
        
        self.allIterations(iteration)

    # Returns the norm for each iteration step
    def getNorms(self, matrices):
        res = []
        for i in range(len(matrices)):
            matrices[i] = json.loads(matrices[i])
            matrices[i] = np.asarray(matrices[i])

            if i > 0:
                res.append(abs(np.linalg.norm(matrices[i] - matrices[i-1])))

        print(res)
        return res
    
    # Returns the eigenvalues for each matrix
    def getEigenvalues(self, matrices):
        res = []
        for i in range(len(matrices)):
            res.append(np.linalg.eigvals(matrices[i]))

        return res
    
    # Returns whether the divergence approaches infinity or repeats
    def isInfiniteDivergence(self, matrices):
        visited = set()
        for matrix in matrices:
            mstr = matrix.tostring()
            print(mstr)
            if mstr in visited:
                return False

            visited.add(mstr)

        return True
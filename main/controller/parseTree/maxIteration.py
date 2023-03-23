from .parseTree import ParseTree
from ...models import Iteration, IterationStep
import json
import numpy as np

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
            startValue = list(json.loads(startValue))
            startValue = np.asarray(startValue)

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
        iteration.save()
        return res
    
    # Based on results checks to see if threshold is reached
    def diverges(self, results, threshold):
        # print(results[len(results)-1] - results[len(results)-2])
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
    
    # returns the value the matrix converged on given an id
    def getConvergeValue(self, id):
        iteration = Iteration.objects.get(pk=id)

        if iteration == None:
            return None
        
        iterationSteps = IterationStep.objects.filter(iterationID=id)
        iterationStep = iterationSteps.get(step=iteration.currentIteration - 1)

        if iterationStep == None:
            return None

        return iterationStep.value
    
    # starts the iteration when given an id
    def startIteration(self, id):
        iteration = Iteration.objects.get(pk=id)

        if iteration == None:
            return
        
        self.allIterations(iteration)


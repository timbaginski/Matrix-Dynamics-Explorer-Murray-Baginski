from ..models import Iteration
from ..controller.parseTree.parseTree import ParseTree

# insert new iteration object into the db so we can start the iteration 
# return the ID
def insertIteration(polynomial, num, maxIter, threshold):
    iteration = Iteration(
        polynomial=polynomial, 
        currentIteration=0, 
        maxIteration=int(maxIter),
        startValue=num,
        threshold=float(threshold),
        converged=False
    )

    iteration.save()
    return iteration.pk 


# start a new iteration given the id of the iteration in the DB 
def startIteration(id):
    iteration = Iteration.objects.get(pk=id)

    if iteration == None:
        return 
    
    tree = ParseTree()
    tree.parsePoly(iteration.polynomial)

    curr = iteration.startValue
    for i in range(iteration.maxIteration):
        nextCurr = tree.callPoly(curr)
        if abs(nextCurr - curr) < iteration.threshold:
            iteration.converged = True
            iteration.convergeValue = curr
            break
        
        curr = nextCurr
        iteration.currentIteration += 1
        iteration.save()

    iteration.save()

# Check the iteration count of a currently running iteration
def getCurrIteration(id):
    iteration = Iteration.objects.get(pk=id)

    if iteration == None:
        return 0
    
    return iteration.currentIteration

# Return the max iteration of a currently running iteration
def getMaxIteration(id):
    iteration = Iteration.objects.get(pk=id)

    if iteration == None:
        return 0
    
    return iteration.maxIteration

# Return whether the current iteration has converged
def getConverged(id):
    iteration = Iteration.objects.get(pk=id)

    if iteration == None:
        return False
    
    return iteration.converged

# Returns an iterations's converge value
def getConvergeValue(id):
    iteration = Iteration.objects.get(pk=id)

    if iteration == None:
        return 0.0
    
    return iteration.convergeValue

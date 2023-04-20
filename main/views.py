from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .controller.parseTree.readMatrices import convert, csvToMatrices
from .controller import iterationController
from .controller.parseTree.parseTree import ParseTree
from .models import Iteration
import threading
import json
from .controller.parseTree.maxIteration import MaxIteration
import numpy as np

# Create your views here.

def index(request):
    return render(request, 'index.html')


def verifyPoly(request):
    polynomial = request.GET.get('polynomial', '')
    tree = ParseTree()
    errorMessage = tree.verifyPoly(polynomial)
    response = {
        'message': errorMessage
    }
    print(errorMessage)
    return JsonResponse(response)

def numberPoly(request):
    polynomial = request.GET.get('polynomial', '')
    num = request.GET.get('num', '')
    maxIter = request.GET.get('maxIter', '')
    threshold = request.GET.get('threshold', '')

    if len(polynomial) == 0 or len(num) == 0 or len(maxIter) == 0 or len(threshold) == 0:
        return index(request)
    
    # insert new iteration into the database
    id = iterationController.insertIteration(polynomial, str(num), maxIter, threshold)

    context = {'id': id}
    return render(request, 'loadingnumber.html', context)


def matrixPoly(request):
    print("new request:")
    print(request.GET)
    polynomial = request.GET.get('polynomial', '')
    matrix = ""
    indices = []
    for i in range(5):
        for j in range(5):
            indices.append(str(j) + str(i))

    for index in indices:
        value = request.GET.get(index, '')
        if value == '':
            continue
        matrix += value + ','

    matrix = matrix[:len(matrix)-1]

    print(matrix)

    matrix = convert(matrix)
    matrix = matrix.tolist()
    matrix = json.dumps(matrix)
    maxIter = request.GET.get('maxIter', '')
    threshold = request.GET.get('threshold', '')

    if len(polynomial) == 0 or len(matrix) == 0 or len(maxIter) == 0 or len(threshold) == 0:
        return index(request)
    
    # insert new iteration into the database
    id = iterationController.insertIteration(polynomial, matrix, maxIter, threshold)

    context = {'id': id}
    return render(request, 'loading.html', context)

def startIteration(request):
    iterationObj = MaxIteration()
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)
    id = body['id']

    # start the process
    x = threading.Thread(target=iterationObj.startIteration, args=(id,))
    x.start()

    return HttpResponse(status=202)


def checkIterationStatus(request):
    iterationObj = MaxIteration()
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)
    id = body['id']
    currIteration = iterationController.getCurrIteration(id)
    maxIteration = iterationController.getMaxIteration(id)
    converged = iterationController.getConverged(id)
    convergeValue = iterationObj.getConvergeValue(id)

    response = {
        'iteration': currIteration,
        'maxIter': maxIteration,
        'converged': converged,
        'convergeValue': convergeValue
    }

    return JsonResponse(response)

def fetchOutput(request):
    iterationObj = MaxIteration()
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)
    id = body['id']
    print(id)
    iterations = iterationController.getAllIterations(id)
    matrices = list(iterations)

    for i in range(len(matrices)):
        matrices[i] = matrices[i].value


    startValue = iterationController.getStartValue(id)
    matrices.insert(0, startValue)

    converged = iterationController.getConverged(id)
    convergeValue = iterationObj.getConvergeValue(id)
    norms = iterationObj.getNorms(matrices)
    eigenvalues = iterationObj.getEigenvalues(matrices)

    for i in range(len(eigenvalues)):
        eigenvalues[i] = list(eigenvalues[i])
        for j in range(len(eigenvalues[i])):
            eigenvalues[i][j] = float( eigenvalues[i][j])
        eigenvalues[i] = json.dumps(eigenvalues[i])

    response = {
        'matrices': json.dumps(norms),
        'converged': converged, 
        'convergeValue': convergeValue,
        'eigenvalues': json.dumps(eigenvalues),
        'infinite': iterationObj.isInfiniteDivergence(matrices)
    }

    return JsonResponse(response)


def csvPoly(request):
    csv = request.FILES['csv']
    matrices = csvToMatrices(csv)
    ids = []

    for matrix in matrices:
        ids.append(iterationController.insertIteration(request.POST["polynomial"], matrix, request.POST["maxIter"], request.POST["threshold"]))

    context = {
        'ids': json.dumps(ids)
    }

    return render(request, 'loadingcsv.html', context)

def output(request):
    ids = [5]
    id = request.GET.get('loadingID', '')

    print("polynomial:")
    #allMatrices = iterationController.getAllIterations(id)
    #id = body['id']
    # ids = getOutput()
    context = {
        'id': id,
    }
    #print(allMatrices)
    #print('id:', id)

    return render(request, 'output.html', context)

def outputcsv(request):
    ids = request.GET.get('loadingID', '')
    
    context = {
        'ids': ids
    }

    return render(request, 'outputcsv.html', context)


def outputnumber(request):
    id = request.GET.get('loadingID', '')
    
    context = {
        'id': id
    }

    return render(request, 'outputnumber.html', context)


def fetchNumber(request):
    iterationObj = MaxIteration()
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)
    id = body['id']

    iterations = iterationController.getAllIterations(id)

    values = []
    for iteration in iterations:
        values.append(iteration.value)

    startValue = iterationController.getStartValue(id)
    values.insert(0, startValue)
    diff = iterationObj.getDifference(values)
    converged = iterationController.getConverged(id)
    convergeValue = iterationObj.getConvergeValue(id)
    infinite = iterationObj.isInfiniteDivergenceNum(values)

    response = {
        'numbers': json.dumps(diff),
        'converged': converged,
        'convergeValue': convergeValue,
        'infinite': infinite
    }

    return JsonResponse(response)



    




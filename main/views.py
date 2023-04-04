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
    return render(request, 'loading.html', context)


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
    #id = request.session.get('id')
    polynomial = request.GET.get('polynomial', '')
    polynomial = '2x'
    #id = iterationController.getLatestIterationByPolynomial(polynomial).id
    print("id")
    print(id)
    polynomial = request.GET.get('polynomial', '')
    print("polynomial:")
    print(polynomial)
   # allMatrices = iterationController.getAllIterations(id)
    num = request.GET.get('num', '')
    maxIter = request.GET.get('maxIter', '')
    threshold = request.GET.get('threshold', '')
    ids.append(polynomial)
    #id = body['id']
    # ids = getOutput()
    context = {
        'id': id,
    }
    print('Context: %s', context)
    print('Request: %s', request)
    print(allMatrices)
    #print('id:', id)

    return render(request, 'output.html', context)




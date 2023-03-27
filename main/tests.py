from django.test import TestCase, Client
from django.db import transaction
from .controller.parseTree.parseTree import ParseTree
import numpy as np
from .controller.parseTree.maxIteration import MaxIteration
from .controller.parseTree.readMatrices import readFile
from .controller.parseTree.outputCsv import toCsv
import json
from .models import Iteration, IterationStep
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile


class ParseTestCase(TestCase):

    # tests parse poly with a simple example
    def testParsePoly(self):
        poly = ParseTree()
        poly.parsePoly(poly='2x + 1')
        ans = poly.callPoly(11)
        self.assertEqual(ans, 23)

    # tests parse poly with parenthesis involved
    def testParsePolyParens(self):
        poly = ParseTree()
        poly.parsePoly(poly='((5 + 6) * x + 2)')
        ans = poly.callPoly(3)
        self.assertEqual(ans, 35)

    # tests parse poly with exponents involved
    def testParsePolyExponents(self):
        poly = ParseTree()
        poly.parsePoly(poly='2x^2 + x')
        ans = poly.callPoly(2)
        self.assertEqual(ans, 10)

    # tests parse poly with subtraction 
    def testParsePolySubtraction(self):
        poly = ParseTree()
        poly.parsePoly(poly='5x - x - 1')
        ans = poly.callPoly(3)
        self.assertEqual(ans, 11)

    # tests parse poly with matrix
    def testParsePolyMat(self):
        poly = ParseTree()
        poly.parsePoly(poly='2x + 1')
        ans = poly.callPoly(np.asarray(a=[[1, 2], [3, 4]]))
        self.assertTrue(np.array_equal(ans, np.asarray(a=[[3, 5], [7, 9]])))

    # tests parse poly with negative
    def testParsePolyMinus(self):
        poly = ParseTree()
        poly.parsePoly(poly='-4x + 1')
        ans = poly.callPoly(2)
        self.assertEqual(ans, -7)

    # test parse poly with more complex negatives
    def testParsePolyAdvanceMinus(self):
        poly = ParseTree()
        poly.parsePoly(poly='5 + -x')
        ans = poly.callPoly(3)
        self.assertEqual(ans, 2)

    # test poly with negative parenthesis
    def testParsePolyNegParen(self):
        poly = ParseTree()
        poly.parsePoly(poly='-(x + 1)')
        ans = poly.callPoly(3)
        self.assertEqual(ans, -4)

    # test poly with division
    def testParsePolyDivision(self):
        poly = ParseTree()
        poly.parsePoly(poly='x / 3')
        ans = poly.callPoly(3)
        self.assertEqual(ans, 1)

    # test poly with multiplication and division
    def testParsePolyMultDiv(self):
        poly = ParseTree()
        poly.parsePoly(poly='x / 3 * 2')
        ans = poly.callPoly(6)
        self.assertEqual(ans, 4)

    def testLastIteration(self):
        iteration = MaxIteration()
        iter = Iteration(polynomial="2x", maxIteration=5, startValue=str(1))
        iter.save()
        ending = iteration.allIterations(iter)[-1]
        self.assertEqual(ending, '32')

    def testFirstIteration(self):
        iteration = MaxIteration()
        iter = Iteration(polynomial="4x", maxIteration=5, startValue=str(1))
        iter.save()
        starting = iteration.allIterations(iter)[0]
        self.assertEqual(starting, '1')

    def testMaxIteration(self):
        iteration = MaxIteration()
        iter = Iteration(polynomial="3x-1", maxIteration=15, startValue=str(1))
        iter.save()
        final = iteration.allIterations(iter)[-1]
        self.assertEqual(final, '7174454')

    def testConvergeIteration(self):
        iteration = MaxIteration()
        iter = Iteration(polynomial="x^0.5", maxIteration=105, startValue=str(.7))
        iter.save()
        computations = iteration.allIterations(iter)
        for i in range(len(computations)):
            computations[i] = float(computations[i])
        doesDiverge = iteration.diverges(computations, .00001)
        self.assertFalse(doesDiverge)

    def testDivergeIteration(self):
        iteration = MaxIteration()
        iter = Iteration(polynomial="2x-1", maxIteration=12, startValue=str(2))
        iter.save()
        computations = iteration.allIterations(iter)
        for i in range(len(computations)):
            computations[i] = int(computations[i])
        doesDiverge = iteration.diverges(computations, 10)
        self.assertTrue(doesDiverge)

    def testMatrixFirstIteration(self):
        iteration = MaxIteration()
        startMatrix = [1,0,0,1]
        iter = Iteration(polynomial="2x", maxIteration=5, startValue=json.dumps(startMatrix))
        iter.save()
        starting = iteration.allIterations(iter)
        starting = json.loads(starting[0])
        self.assertEqual(starting, startMatrix)

    def testMatrixLastIteration(self):
        iteration = MaxIteration()
        startMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        last = 15
        iter = Iteration(polynomial="2x", maxIteration=last, startValue=json.dumps(startMatrix))
        iter.save()
        secondMatrix = [[2**last, 0.0, 0.0], [0.0, 2**last, 0.0], [0.0, 0.0, 2**last]]
        matrices = iteration.allIterations(iter)
        self.assertTrue(np.array_equal(json.loads(matrices[-1]), secondMatrix))

    def testFirstCsvFirstIteration(self):
        iteration = MaxIteration()
        matrices = readFile("testIdentities.csv")
        matrix = matrices[0].tolist()
        iter = Iteration(polynomial="x", maxIteration=1, startValue=json.dumps(matrix))
        iter.save()
        allMatrices = iteration.allIterations(iter)
        self.assertTrue(np.array_equal(json.loads(allMatrices[0]), np.asarray(matrix)))

    def testFirstCsvLastIteration(self):
        iteration = MaxIteration()
        matrices = readFile("testIdentities.csv")
        lastMatrix = [[float(4**5), 0.0, 0.0], [0.0, float(4**5), 0.0], [0.0, 0.0, float(4**5)]]
        matrix = matrices[0].tolist()
        last = 5
        iter = Iteration(polynomial="4x", maxIteration=last, startValue=json.dumps(matrix))
        iter.save()
        allMatrices = iteration.allIterations(iter)
        last = allMatrices[-1]
        last = json.loads(last)
        last = np.asarray(last)
        lastMatrix = np.asarray(lastMatrix)
        self.assertTrue(np.array_equal(last, lastMatrix))

    def testLastCsvLastIteration(self):
        iteration = MaxIteration()
        matrices = readFile("testIdentities.csv")
        last = 5
        lastMatrix = [[float(3*2**last), 0.0, 0.0], [0.0, float(3*2**last), 0.0], [0.0, 0.0, float(3*2**last)]]
        startMatrix = matrices[-1].tolist()
        iter = Iteration(polynomial="2x", maxIteration=last, startValue=json.dumps(startMatrix))
        iter.save()
        allMatrices = iteration.allIterations(iter)
        lastMatrix = np.asarray(lastMatrix)
        first = allMatrices[-1]
        first = json.loads(first)
        first = np.asarray(first)
        self.assertTrue(np.array_equal(first, lastMatrix))

    def testMatrixConverges(self):
        pass
        #iteration = MaxIteration()
        #startMatrix = [[.87, 0, 0], [0, .87, 0], [0, 0, .87]]
        #iter = Iteration(polynomial="x^0.5", maxIteration=15, startValue=json.dumps(startMatrix))
        #iter.save()
        #matrices = iteration.allIterations(iter)
        #doesDiverge = iteration.diverges(matrices, .00001)
        #self.assertFalse(doesDiverge.any())

    def testMatrixDiverges(self):
        pass
        #iteration = MaxIteration()
        #startMatrix = [[.87, .8, .93], [.65, .97, 1.04], [.99, .18, .9]]
        #iter = Iteration(polynomial="x^2", maxIteration=15, startValue=json.dumps(startMatrix))
        #iter.save()
        #matrices = iteration.allIterations(iter)
        #for i in range(len(matrices)):
            #matrices[i] = 
        #doesDiverge = iteration.diverges(matrices, 1)
        #self.assertTrue(doesDiverge.any())

    def testOutputToCsv(self):
        pass
        #iteration = MaxIteration()
        #startMatrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        #iter = Iteration(polynomial="2x", maxIteration=28, startValue=json.dumps(startMatrix))
        #iter.save()
        #allMatrices = iteration.allIterations(iter)
        #toCsv(allMatrices, "outputTest.csv")

    def testInputToCsv(self):
        iteration = MaxIteration()
        matrices = readFile("testIdentities.csv")
        values = []
        for matrix in matrices:
            iter = Iteration(polynomial="2x", maxIteration=5, startValue=json.dumps(matrix.tolist()))
            iter.save()
            allMatrices = iteration.allIterations(iter)
            values.append(allMatrices)
        toCsv(values, "bigOutputTest.csv")

class ViewsTestCase(TestCase):

    # test whether Views can return the index page
    def testGetIndex(self):
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)

    # test whether Views can successfully validate a correctly formatted polynomial
    def testValidatePoly(self):
        c = Client()
        response = c.get('/verifyPoly/?polynomial=x%20%2B%203')
        content = response.content.decode('utf-8')
        content = json.loads(content)
        self.assertEqual(content['message'], 'Valid')

    # test whether Views can successfully identify an empty poly
    def testEmptyPoly(self):
        c = Client()
        response = c.get('/verifyPoly/?polynomial=')
        content = response.content.decode('utf-8')
        content = json.loads(content)
        self.assertEqual(content['message'], 'Polynomial Cannot be Empty')

    # test whether Views can successfully spot a poly with an invalid token
    def testInvalidToken(self):
        c = Client()
        response = c.get('/verifyPoly/?polynomial=y%20%2B%203')
        content = response.content.decode('utf-8')
        content = json.loads(content)
        self.assertEqual(content['message'], 'Invalid Token Error')

    # test whether Views can successfully spot an invalid operation 
    def testInvalidOperation(self):
        c = Client()
        response = c.get('/verifyPoly/?polynomial=x%20%2B%20^%203')
        content = response.content.decode('utf-8')
        content = json.loads(content)
        self.assertEqual(content['message'], 'Invalid Operation Error')

    # test whether views can insert a Poly into the db and return loading page
    def testInsertPoly(self):
        c = Client()
        response = c.get('/numberPoly/?polynomial=x%20%2B%203&num=1&maxIter=100&threshold=0.1')
        self.assertEqual(response.status_code, 200)

    # test whether we can start an iteration for an inserted polynomial
    @transaction.atomic
    def testStartIteration(self):
        # insert a poly
        c = Client()
        response = c.get('/numberPoly/?polynomial=x%20%2B%203&num=1&maxIter=100&threshold=0.1')

        # get id from response
        response_str = response.content.decode()
        response_id_index = response_str.index('let id = ')
        id_str = ""
        reached_quote = False 
        while response_id_index < len(response_str):
            if reached_quote and response_str[response_id_index] == '"':
                break
            elif response_str[response_id_index] == '"':
                reached_quote = True
            elif reached_quote:
                id_str += response_str[response_id_index]

            response_id_index += 1

        response = c.post('/startIteration/', json.dumps({'id': id_str}), content_type='application/json')
        status = response.status_code
        print("my status:")
        print(status)
        self.assertEqual(status, 202)

    def testCsvPoly(self):
        c = Client()
        with open('testIdentities.csv', 'r') as f:
            postResponse = c.post('/csvPoly/',
                {
                    'polynomial': '5x',
                    'maxIter': '10',
                    'threshold': '.2',
                    'csv': InMemoryUploadedFile(f, "file_content", 'testIdentities.csv', 'csv', 5000, 0),
                }
            )
        self.assertEqual(postResponse.status_code, 200)

    def testMatrixPoly(self):
        c = Client()
        #response = c.get('/matrixPoly/?polynomial=x%20%2B%203&MATRIX&maxIter=100&threshold=0.1')
        getResponse = c.get('/matrixPoly/',
                {
                    'polynomial': '5x',
                    'maxIter': '10',
                    'threshold': '.2',
                    '00': '1',
                    '01': '0',
                    '10': '0',
                    '11': '1'
                })
        self.assertEqual(getResponse.status_code, 200)







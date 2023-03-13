from django.test import TestCase, Client
from .controller.parseTree.parseTree import ParseTree
import numpy as np
from .controller.parseTree.maxIteration import maxIteration
from .controller.parseTree.readMatrices import readFile
from .controller.parseTree.outputCsv import toCsv
import json


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
        iteration = maxIteration()
        ending = iteration.allIterations(polynomial="2x", maxVal = 5, startVal = 1)[5]
        self.assertEqual(ending, 32)

    def testFirstIteration(self):
        iteration = maxIteration()
        starting = iteration.allIterations(polynomial="4x", maxVal = 5, startVal = 1)[0]
        self.assertEqual(starting, 1)

    def testMaxIteration(self):
        iteration = maxIteration()
        final = iteration.allIterations(polynomial="3x-1", maxVal = 15, startVal = 1)[15]
        self.assertEqual(final, 7174454)

    def testConvergeIteration(self):
        iteration = maxIteration()
        computations = iteration.allIterations(polynomial="x^.5", maxVal = 150, startVal = .7)
        doesDiverge = iteration.diverges(computations, .00001)
        self.assertFalse(doesDiverge)

    def testDivergeIteration(self):
        iteration = maxIteration()
        computations = iteration.allIterations(polynomial="2x-1", maxVal = 12, startVal = 2)
        doesDiverge = iteration.diverges(computations, 10)
        self.assertTrue(doesDiverge)

    def testMatrixFirstIteration(self):
        iteration = maxIteration()
        startMatrix = [1,0,0,1]
        starting = iteration.allIterations(polynomial="2x", maxVal = 5, startVal = startMatrix)[0]
        self.assertEqual(starting, startMatrix)

    def testMatrixLastIteration(self):
        iteration = maxIteration()
        startMatrix = np.asarray(a=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        last = 15
        secondMatrix = np.asarray(a=[[4**last, 0, 0], [0, 4**last, 0], [0, 0, 4**last]])
        matrices = iteration.allIterations(polynomial="4x", maxVal = last, startVal = startMatrix)
        self.assertTrue(np.array_equal(matrices[last], secondMatrix))

    def testFirstCsvFirstIteration(self):
        iteration = maxIteration()
        matrices = readFile("testIdentities.csv")
        matrix = matrices[0]
        allMatrices = iteration.allIterations(polynomial="2x", maxVal = 1, startVal = matrix)
        self.assertTrue(np.array_equal(allMatrices[0], matrix))

    def testFirstCsvLastIteration(self):
        iteration = maxIteration()
        matrices = readFile("testIdentities.csv")
        lastMatrix = [[4**5, 0, 0], [0, 4**5, 0], [0, 0, 4**5]]
        matrix = matrices[0]
        last = 5
        allMatrices = iteration.allIterations(polynomial="4x", maxVal = last, startVal = matrix)
        self.assertTrue(np.array_equal(allMatrices[last], lastMatrix))

    def testLastCsvLastIteration(self):
        iteration = maxIteration()
        matrices = readFile("testIdentities.csv")
        last = 5
        lastMatrix = [[3*2**last, 0, 0], [0, 3*2**last, 0], [0, 0, 3*2**last]]
        startMatrix = matrices[-1]
        allMatrices = iteration.allIterations(polynomial="2x", maxVal = last, startVal = startMatrix)
        self.assertTrue(np.array_equal(allMatrices[last], lastMatrix))

    def testMatrixConverges(self):
        iteration = maxIteration()
        startMatrix = np.asarray(a=[[.87, 0, 0], [0, .87, 0], [0, 0, .87]])
        matrices = iteration.allIterations(polynomial="x^.5", maxVal = 15, startVal = startMatrix)
        doesDiverge = iteration.diverges(matrices, .00001)
        self.assertFalse(doesDiverge.any())

    def testMatrixDiverges(self):
        iteration = maxIteration()
        startMatrix = np.asarray(a=[[.87, .8, .93], [.65, .97, 1.04], [.99, .18, .9]])
        matrices = iteration.allIterations(polynomial="x^2", maxVal = 15, startVal = startMatrix)
        doesDiverge = iteration.diverges(matrices, 1)
        self.assertTrue(doesDiverge.any())

    def testOutputToCsv(self):
        iteration = maxIteration()
        startMatrix = np.asarray(a=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        allMatrices = iteration.allIterations(polynomial="2x", maxVal = 28, startVal = startMatrix)
        toCsv(allMatrices, "outputTest.csv")

    def testInputToCsv(self):
        iteration = maxIteration()
        matrices = readFile("testIdentities.csv")
        values = []
        for matrix in matrices:
            allMatrices = iteration.allIterations(polynomial="2x", maxVal = 28, startVal = matrix)
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

        #response = c.post('/startIteration/', json.dumps({'id': id_str}), content_type='application/json')
        #self.assertEqual(response.status_code, 202)








from django.test import TestCase
from .controller.parseTree.parseTree import ParseTree
import numpy as np
from .controller.parseTree.maxIteration import maxIteration
from .controller.parseTree.readMatrices import readFile

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






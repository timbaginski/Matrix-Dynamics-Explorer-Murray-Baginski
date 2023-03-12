from django.test import TestCase
from .controller.parseTree.parseTree import ParseTree
import numpy as np

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

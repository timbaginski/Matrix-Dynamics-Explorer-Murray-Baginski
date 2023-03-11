from .additionNode import AdditionNode
from .subtractionNode import SubtractionNode
from .multiplicationNode import MultiplicationNode
from .exponentNode import ExponentNode
from .constantNode import ConstantNode
from .variableNode import VariableNode

class ParseTree():

    def __init__(self):
        self.root = None
    
    # Matrix polynomial needs different cleaning
    def cleanPoly(self, poly: str):
        # remove whitespace
        poly = poly.replace(" ", "")

        # add implicit multiplication signs
        # turn negative x into -1 * x
        # We iterate through second to last index because last index can't be being multiplied
        newPoly = ""
        for i in range(len(poly) - 1):
            if poly[i].isdigit() and (poly[i+1] == 'x' or poly[i+1] == '('):
                newPoly += poly[i] + '*'
            elif poly[i] == ')' and (poly[i+1] == 'x' or poly[i+1].isdigit() or poly[i+1] == '.'):
                newPoly += poly[i] + '*'
            elif i > 0 and poly[i] == '-' and poly[i-1] == '+':
                newPoly = newPoly[:len(newPoly)-1] + '-'
            elif i > 0 and poly[i] == '-' and poly[i-1] == '-':
                newPoly = newPoly[:len(newPoly)-1] + '+'
            elif poly[i] == '-' and (i == 0 or (not poly[i-1].isdigit())) and (poly[i+1] == 'x' or poly[i+1] == '('):
                newPoly += '-1*'
            else:
                newPoly += poly[i]
        

        newPoly += poly[-1]
        return [x for x in newPoly]
    
    # figures out if a polynomial is inside parenthesis
    # creates a queue of open parenthesis and pops the paren whenever it is closed
    # if the open paren at the start of the poly is still there at the last element, 
    # this means the entire statement is in parenthesis
    def inParens(self, poly: list[str]) -> bool:
        if len(poly) < 2 or poly[0] != '(':
            return False 
        
        queue = [0]
        for i in range(1, len(poly)-1):
            if poly[i] == '(':
                queue.append(i)
            if poly[i] == ')':
                queue.pop()

        return len(queue) > 0 and queue[0] == 0
    

    # Given a poly, remove all parenthesis that surround the entire statement
    def removeRedundentParens(self, poly: list[str]):
        while self.inParens(poly):
            # if we are inside parens we remove the last 2 element (the parens)
            # We loop because there could be multiple layers
            poly.pop(0)
            poly.pop()

        return poly
    

    # finds the "lowest priority" operation in a polynomial and returns the operator's index
    def findLowestOp(self, poly):
        parens = 0
        operators = dict()
        signs = ['+', '-', '*', '^']
        
        for index, c in enumerate(poly):
            if index == 0 and c == '-':
                continue
            if index > 0 and c in operators and poly[index-1] in operators:
                continue
            if c in signs and parens <= 0:
                operators[c] = index

            if c == '(':
                parens += 1 
            
            if c == ')':
                parens -= 1

        if '+' in operators and '-' in operators:
            return operators['+'] if operators['+'] >= operators['-'] else operators['-']

        if '+' in operators:
            return operators['+']
        
        if '-' in operators:
            return operators['-']
        
        if '*' in operators:
            return operators['*']
        
        if '^' in operators:
            return operators['^']
        
        return -1
    
    # based on the type of the lowest priority operation, we create a new node
    def getNode(self, op):
        if op == '+':
            return AdditionNode()
        
        if op == '-':
            return SubtractionNode()
        
        if op == '*':
            return MultiplicationNode()
        
        if op == '^':
            return ExponentNode()
 
    # recursively builds the parse tree from a polynomial represented as list of characters
    def createTree(self, poly: list[str]):
        # remove parens around entire statement
        poly = self.removeRedundentParens(poly)

        # next, check if this poly is a number. If so, we return a ConstantNode
        polyStr = ''.join(poly)

        if len(polyStr) > 0 and (polyStr.isdigit() or (polyStr[0] == '-' and polyStr[1:].isdigit())):
            return ConstantNode(val=int(polyStr))

        if len(polyStr) > 0 and (polyStr.replace(".", "").isnumeric() or (polyStr[0] == '-' and polyStr[1:].replace(".", "").isnumeric())):
            return ConstantNode(val=float(polyStr))
    
        # now, check if the poly is a variable. If so, we return a VariableNode
        if len(poly) == 1 and poly[0] == 'x':
            return VariableNode()
        
        # with the leaves out of the way, we want to find the lowest priority operation 
        lowestOpIndex = self.findLowestOp(poly)

        # now, based on the sign of our operation we select the correct Node type
        parent = self.getNode(poly[lowestOpIndex])

        # finally, recursively call createTree to build parent's left and right subtrees
        parent.left = self.createTree(poly[:lowestOpIndex])
        parent.right = self.createTree(poly[lowestOpIndex+1:])

        return parent
    

    def parsePoly(self, poly: str):
        poly = self.cleanPoly(poly)
        self.root = self.createTree(poly)


    # Takes a x value and plugs it into the poly, returning the result
    def callPoly(self, x):
        return self.root.getVal(x)
    
    # Called by level order
    def bfs(self, queue, res):
        if len(queue) == 0:
            return 
        
        temp = queue.pop(0)
        node, level = temp[0], temp[1]

        if node == None:
            return 

        if len(res) == level:
            res.append([str(node)])
        else:
            res[-1].append(str(node))
        
        node.insertInOrder(queue, level)

        self.bfs(queue, res)

    # helper for bfs
    def levelOrder(self):
        queue = [[self.root, 0]]
        res = []
        self.bfs(queue, res)
        return res

from .node import Node
import numpy as np

# SubtractionNode is a subclass of Node
class SubtractionNode(Node):

    def getVal(self, x):
        leftVal, rightVal = 0, 0
        if self.left != None:
            leftVal = self.left.getVal(x)

        if self.right != None:
            rightVal = self.right.getVal(x)

        if type(leftVal) != np.array and type(rightVal) != np.array:
            return leftVal - rightVal
        
        if type(leftVal) != np.array:
            leftVal = np.multiply(leftVal, np.identity(n=x.shape()[0]))

        if type(rightVal) != np.array:
            rightVal = np.multiply(rightVal, np.identity(n=x.shape()[0]))

        return np.subtract(leftVal, rightVal)
    
    def __str__(self):
        return '-'
    
    def insertInOrder(self, queue, level):
        queue.append([self.left, level+1])
        queue.append([self.right, level+1])
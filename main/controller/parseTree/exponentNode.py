from .node import Node 
import numpy as np 
from scipy.linalg import fractional_matrix_power

# ExponentNode is a subclass of Node
class ExponentNode(Node):

    def getVal(self, x):
        leftVal, rightVal = 0, 0
        if self.left != None:
            leftVal = self.left.getVal(x)

        if self.right != None:
            rightVal = self.right.getVal(x)

        if type(leftVal) != np.ndarray:
            return leftVal ** rightVal
        
        if type(rightVal) == float:
            return fractional_matrix_power(leftVal, rightVal)

        return np.linalg.matrix_power(leftVal, rightVal)
    
    def __str__(self):
        return '^'
    
    def insertInOrder(self, queue, level):
        queue.append([self.left, level+1])
        queue.append([self.right, level+1])
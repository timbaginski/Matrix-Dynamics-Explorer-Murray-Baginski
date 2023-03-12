from .node import Node

# DivisionNode is a subclass of node
class DivisionNode(Node):

    def getVal(self, x):
        leftVal, rightVal = 0, 1
        if self.left != None:
            leftVal = self.left.getVal(x)
        
        if self.right != None:
            rightVal = self.right.getVal(x)

        return leftVal / rightVal
    
    def __str__(self):
        return '/'
    
    def insertInOrder(self, queue, level):
        queue.append([self.left, level+1])
        queue.append([self.right, level+1])
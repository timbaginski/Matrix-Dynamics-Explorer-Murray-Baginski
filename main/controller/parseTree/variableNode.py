from .node import Node 

# VariableNode is a leaf node who's value is a variable. It returns the variable passed to getVal
class VariableNode(Node):
    # VariableNode has no value, left, or right 
    def __init__(self):
        pass

    def getVal(self, x):
        return x
    
    def __str__(self):
        return 'x'
    
    def insertInOrder(self, queue, level):
        return


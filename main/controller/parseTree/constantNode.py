from .node import Node

# ConstantNode is a subclass of Node
class ConstantNode(Node):
    # ConstantNode has a value, but no left or right
    def __init__(self, val=None):
        self.val = val 

    def getVal(self, x):
        return self.val
    
    def __str__(self):
        return str(self.val)
    
    def insertInOrder(self, queue, level):
        return
  

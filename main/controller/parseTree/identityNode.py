from .node import Node 
import numpy as np 

# Identity node is a subclass of Node
class IdentityNode(Node):
    # IdentityNode has no value, left, or right 
    def __init__(self):
        pass
    
    # returns the identity matrix with the same shape as x
    def getVal(self, x):
        if type(x) != np.array:
            return None 
        
        return np.identity(n=x.shape()[0])
    

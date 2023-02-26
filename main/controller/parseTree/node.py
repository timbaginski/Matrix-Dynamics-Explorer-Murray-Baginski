from __future__ import annotations
from abc import ABC, abstractmethod


# parent class for each Node type
class Node(ABC):
    # a Node doesn't have a value, because only the leaf child class needs one
    def __init__(self, left: Node=None, right: Node=None):
        self.left = left 
        self.right = right

    @abstractmethod
    def getVal(self, x):
        pass

    @abstractmethod
    def insertInOrder(queue, level):
        pass

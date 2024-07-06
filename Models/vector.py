import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, scalar: float):
        self.x = self.x * scalar
        self.y = self.y * scalar
        
        
    def __div__(self, scalar: float):
        self.x = self.x/scalar
        self.y = self.y/scalar
    
    
    def set_module(self, mod: float):
        self.__div__(self.module)
        self.__mul__(mod)        
    
    def module(self):
        return math.sqrt(self.prod_int(self, self))
    
    def prod_int(v1, v2):
        return v1.x * v2.x + v1.y * v2.y
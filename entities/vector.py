import math

class Vector:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
        
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        self.
        self.x = self.x * scalar
        self.y = self.y * scalar
            
    def __div__(self, scalar: float):
        self.x = self.x/scalar
        self.y = self.y/scalar
        
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
    
    def set_module(self, mod: float):
        self.__div__(self.module())
        self * mod        
    
    def module(self):
        return math.sqrt(Vector.prod_int(self, self))
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def reflect(self, normal):
        dot_product = self.dot(normal)
        return Vector(self.x - 2 * dot_product * normal.x, self.y - 2 * dot_product * normal.y)
    
    @staticmethod
    def prod_int(v1, v2):
        return v1.x * v2.x + v1.y * v2.y
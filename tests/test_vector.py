import unittest
import math
from entities.vector import Vector

class TestVector(unittest.TestCase):

    def setUp(self):
        self.vector1 = Vector(3, 4)
        self.vector2 = Vector(1, 2)
    
    def test_sub(self):
        result = self.vector1 - self.vector2
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 2)
    
    def test_add(self):
        result = self.vector1 + self.vector2
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)
    
    def test_mul(self):
        self.vector1 * 2
        self.assertEqual(self.vector1.x, 6)
        self.assertEqual(self.vector1.y, 8)
    
    def test_div(self):
        self.vector1.__div__(2)
        self.assertEqual(self.vector1.x, 1.5)
        self.assertEqual(self.vector1.y, 2)
    
    def test_length(self):
        self.assertEqual(self.vector1.length(), 5)
    
    def test_normalize(self):
        self.vector1.normalize()
        self.assertAlmostEqual(self.vector1.x, 0.6)
        self.assertAlmostEqual(self.vector1.y, 0.8)
    
    def test_set_module(self):
        self.vector1.set_module(10)
        self.assertAlmostEqual(self.vector1.length(), 10)
    
    def test_module(self):
        self.assertEqual(self.vector1.module(), 5)
    
    def test_dot(self):
        result = self.vector1.dot(self.vector2)
        self.assertEqual(result, 11)
    
    def test_prod_int(self):
        result = Vector.prod_int(self.vector1, self.vector2)
        self.assertEqual(result, 11)

if __name__ == '__main__':
    unittest.main()

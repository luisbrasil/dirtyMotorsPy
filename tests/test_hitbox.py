import unittest

from entities.hitbox import Hitbox
from entities.object import Object
from entities.vector import Vector


class TestHitbox(unittest.TestCase):
    
    def setUp(self):
        self.hitbox1 = Hitbox(19, 20, 10, Object(Vector(3, 4), Vector(3, 4), 24))
        self.hitbox2 = Hitbox(10, 10, 5, Object(Vector(1, 2), Vector(1, 2), 12))

    def test_check_collision(self):
        result = self.hitbox1.check_collision(self.hitbox2)
        self.assertFalse(result)
        
if __name__ == '__main__':
    unittest.main()
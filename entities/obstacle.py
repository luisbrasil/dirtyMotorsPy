import math
from entities.vector import Vector
from entities.object import Object
from systems.image_rendering import blit_rotate_center


class Obstacle(Object):
    START_POS = (150, 150)

    def __init__(self, image):
        super().__init__(Vector(*self.START_POS), Vector(0, 0))
        self.img = image
        

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(0))
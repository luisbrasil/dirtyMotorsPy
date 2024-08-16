import math
from entities.hitbox import Hitbox
from entities.vector import Vector
from entities.object import Object
from systems.image_rendering import blit_rotate_center


class Obstacle(Object):
    START_POS = (150, 150)

    def __init__(self, image, mass):
        super().__init__(Vector(*self.START_POS), Vector(0, 0), mass)
        self.hitbox = Hitbox(19, 20, 20, self)
        self.img = image
        

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(0))

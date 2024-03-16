from Models.object import Object
from Models.point import Point
from Models.vector import Vector


class Car(Object):
    START_POS = (0, 0)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(Point(*self.START_POS), Vector(0, 0))
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
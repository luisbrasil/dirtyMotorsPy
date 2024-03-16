import math
from Models.object import Object
from Models.point import Point
from Models.vector import Vector
from utils import blit_rotate_center


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
            
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.point.y -= vertical
        self.point.x -= horizontal
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

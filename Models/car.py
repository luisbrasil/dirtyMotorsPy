import math
from Models.object import Object
from Models.vector import Vector
from utils import blit_rotate_center
from utils import scale_image
import pygame

class Car(Object):
    START_POS = (0, 0)
    DIRECTION_RIGHT = Vector(1,0)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(Vector(*self.START_POS), Vector(0, 0))
        self.max_vel = max_vel
        self.vel = 0
        self.direction= self.DIRECTION_RIGHT
        self.rotation_vel = math.radians(rotation_vel)
        self.angle = 0
        self.acceleration = 0.1
        self.img = scale_image(pygame.image.load("./sprites/BlackOut.png"), 0.55)

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

        # self.angle já está em radianos
        xDir = math.cos(self.angle) * self.DIRECTION_RIGHT.x - \
            math.sin(self.angle) * self.DIRECTION_RIGHT.y
        yDir = math.sin(self.angle) * self.DIRECTION_RIGHT.x + \
            math.cos(self.angle) * self.DIRECTION_RIGHT.y
            
        self.direction.x = xDir
        self.direction.y = yDir

    def physics(self, time:float):
        self.speed = self.direction 
        self.speed.set_module(self.vel)
        super().physics(time)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        self.position.x += self.vel * math.cos(self.angle)
        self.position.y += self.vel * math.sin(self.angle)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2,
                       0) if self.vel > 0 else min(self.vel + self.acceleration / 2, 0)
        self.move()

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(
            self.angle))  # Converte o ângulo para graus ao desenhar

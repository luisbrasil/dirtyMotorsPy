import math
import pygame
from Models.object import Object
from Models.vector import Vector
from utils import blit_rotate_center
from utils import scale_image

class Car(Object):
    START_POS = (0, 0)
    DIRECTION_RIGHT = Vector(1,0)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(Vector(*self.START_POS), Vector(0, 0))
        self.max_vel = max_vel
        self.vel = 0
        self.direction = Vector(1,0)
        self.rotation_vel = 3.14/4
        self.angle = 0
        self.acceleration = 5
        self.img = scale_image(pygame.image.load("./sprites/BlackOut.png"), 0.55)

    def rotate(self, time:float, left=False, right=False):
        if left:
            self.angle += self.rotation_vel * time
        elif right:
            self.angle -= self.rotation_vel * time

        cosAngle = math.cos(self.angle)
        sinAngle = math.sin(self.angle)
        # self.angle já está em radianos
        xDir = cosAngle * self.DIRECTION_RIGHT.x - sinAngle * self.DIRECTION_RIGHT.y
        yDir = sinAngle * self.DIRECTION_RIGHT.x + cosAngle * self.DIRECTION_RIGHT.y

        self.direction.x = xDir
        self.direction.y = yDir

    def physics(self, time:float):
        if(self.vel == 0):
            self.speed = Vector(0,0)
        else:
            self.speed = self.direction 
            self.speed.set_module(self.vel)
            
        super().physics(time)

    def move_forward(self, time):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        #print('Velocidade modular: ' + str(self.vel))

    def move_backward(self, time):
        acceleration = (5 if self.vel > 0 else 1) * self.acceleration
        self.vel = max(self.vel - acceleration, -self.max_vel / 2)

    def reduce_speed(self, time):
        self.vel = max(self.vel - self.acceleration / 2,
                       0) if self.vel > 0 else min(self.vel + self.acceleration / 2, 0)

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(
            self.angle))  # Converte o ângulo para graus ao desenhar

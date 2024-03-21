import math
from Models.object import Object
from Models.vector import Vector
from utils import blit_rotate_center


class Car(Object):
    START_POS = (0, 0)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(Vector(*self.START_POS), Vector(0, 0))
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = 0.1

    # Pegar o tempo de cada frame para multiplicar a velocidade angular
    def rotate(self, left=False, right=False):
        deltaAngle = self.rotation_vel
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        
        xSpeed = math.cos(deltaAngle) * self.speed.x + math.sin(deltaAngle) * self.speed.y
        ySpeed = - math.sin(deltaAngle) * self.speed.x + math.cos(deltaAngle) * self.speed.y
        self.speed.x = xSpeed
        self.speed.y = ySpeed
            
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
        
    # A propriedade self.angle em si já deve ser um radiano, não converte-lo
    # Pegar o tempo de cada frame para multiplicar
    def move(self):
        self.position.y += self.speed.y
        self.position.x += self.speed.x
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

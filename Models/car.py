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
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        
        xSpeed = math.cos(self.angle) * self.speed.x + \
            math.sin(self.angle) * self.speed.y
        ySpeed = - math.sin(self.angle) * self.speed.x + \
            math.cos(self.angle) * self.speed.y
        self.speed.x = xSpeed
        self.speed.y = ySpeed
            
    def move_forward(self):
        self.speed.x = min(self.speed.x + self.acceleration, self.max_vel)
        self.speed.y = min(self.speed.y + self.acceleration, self.max_vel)
        self.move()
        
    def move_backward(self):
        self.speed.x = max(self.speed.x - self.acceleration, -self.max_vel/2)
        self.speed.y = max(self.speed.y - self.acceleration, -self.max_vel/2)
        self.move()
        
    # A propriedade self.angle em si já deve ser um radiano, não converte-lo
    # Pegar o tempo de cada frame para multiplicar
    def move(self):
        self.position.y += self.speed.y
        self.position.x += self.speed.x
        
    def reduce_speed(self):
        self.speed.x = max(self.speed.x - self.acceleration / 2, 0)
        self.speed.y = max(self.speed.y - self.acceleration / 2, 0)
        self.move()

    def draw(self, win):
        blit_rotate_center(
            win, self.img, (self.position.x, self.position.y), self.angle)

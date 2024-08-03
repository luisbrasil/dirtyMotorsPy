import math
import pygame
from entities.object import Object

class Hitbox:
    def __init__(self, x, y, radius, object : Object):
        self.x = x
        self.y = y 
        self.radius = radius
        self.object = object
         
    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.object.x + self.x, self.object.y + self.y), self.radius, 2)
        
    def check_collision(self, other):
        dx = (self.object.position.x + self.x) - (other.object.position.x + other.x)
        dy = (self.object.position.y + self.y) - (other.object.position.y + other.y)
        distance = math.sqrt(dx**2 + dy**2)

        return distance < (self.radius + other.radius)

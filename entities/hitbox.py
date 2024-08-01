import pygame



class Hitbox:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y 
        self.radius = radius
         
    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius, 2)
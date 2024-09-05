import pygame
import math


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move o tiro na direção do ângulo
        self.x += self.speed * math.cos(self.angle)
        self.y -= self.speed * math.sin(self.angle)
        self.rect.center = (self.x, self.y)

    def __str__(self):
        return f"Bullet(position=({self.x:.2f}, {self.y:.2f}), angle={self.angle:.2f})"

import pygame

from entities.object import Object


class Bullet(Object):
    def __init__(self, direction, pos, speed, mass):
        super().__init__(pos, speed, mass)
        self.direction = direction
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.x = 0
        self.y = 0

    def update(self):
        # Atualiza a posição do projétil com base no vetor de direção e velocidade
        self.x += self.direction.x * self.speed
        self.y -= self.direction.y * self.speed
        self.rect.center = (self.x, self.y)

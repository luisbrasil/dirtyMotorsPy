import pygame


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Atualiza a posição do projétil com base no vetor de direção e velocidade
        self.x += self.direction.x * self.speed
        self.y -= self.direction.y * self.speed
        self.rect.center = (self.x, self.y)

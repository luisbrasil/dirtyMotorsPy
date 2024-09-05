import os
import pygame

from entities.object import Object


class Bullet(Object):
    def __init__(self, direction, pos, speed, mass):
        super().__init__(pos, speed, mass)
        self.direction = direction
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        
        self.laser_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'laser.mp3'))

        self.play_laser_sound()
        
    def play_laser_sound(self):
        self.laser_sound.play()

    def update(self):
        self.position.x += self.direction.x * self.speed
        self.position.y -= self.direction.y * self.speed
        self.rect.center = (self.position.x, self.position.y)

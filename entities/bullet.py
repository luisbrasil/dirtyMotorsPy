import math
import os
import pygame
from entities.hitbox import Hitbox
from systems.image_rendering import blit_rotate_center

from entities.object import Object


class Bullet(Object):
    def __init__(self, direction, pos, speed, mass,angle):
        super().__init__(pos, speed, mass)
        self.direction = direction
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.speed = speed
        self.angle = angle
        self.hitbox = Hitbox(0, 0, 5, self)
        
        self.laser_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'laser.mp3'))

        self.play_laser_sound()
        
    def play_laser_sound(self):
        self.laser_sound.play()
    
    def draw(self, win):
        blit_rotate_center(win, self.image, (self.position.x,
                           self.position.y), math.degrees(self.angle))


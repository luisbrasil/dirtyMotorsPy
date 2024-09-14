import copy
import math
import os
import pygame
from entities.hitbox import Hitbox
from entities.vector import Vector
from systems.image_rendering import blit_rotate_center

from entities.object import Object


class Bullet(Object):
    def __init__(self, car):
        shootPosition = Vector(car.position.x + car.direction.x, car.position.y + car.direction.y)
        super().__init__(shootPosition, Vector(car.direction.x * 1000, car.direction.y * 1000), 10)
        self.direction = copy.copy(car.direction)
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Cor do tiro (vermelho)
        self.angle = copy.copy(car.angle)
        self.hitbox = Hitbox(0, 0, 5, self)
        self.car = car
        
        self.laser_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'laser.mp3'))

        self.play_laser_sound()
        
    def play_laser_sound(self):
        self.laser_sound.play()
        
    def physics(self, time: float):
        self.check_left_screen()
        super().physics(time)
        
    def check_left_screen(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if self.position.x > screen_width + 0.03 * screen_width:
            self.car.bullets.remove(self)
            self.dispose = True
        elif self.position.x < 0 - 0.03 * screen_width:
            self.car.bullets.remove(self)
            self.dispose = True
        if self.position.y > screen_height + 0.03 * screen_height:
            self.car.bullets.remove(self)
            self.dispose = True
        elif self.position.y < 0 - 0.03 * screen_height:
            self.car.bullets.remove(self)
            self.dispose = True
    
    def draw(self, win):
        blit_rotate_center(win, self.image, (self.position.x,
                           self.position.y), math.degrees(self.angle))


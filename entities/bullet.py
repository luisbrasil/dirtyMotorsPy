import copy
import math
import os
import pygame
from components.assets_port import AssetsPort
from entities.hitbox import Hitbox
from entities.vector import Vector
from systems.image_rendering import blit_rotate_center

from entities.object import Object


class Bullet(Object):
    def __init__(self, car):
        shoot_position = Vector(car.position.x + car.direction.x, car.position.y + car.direction.y)
        super().__init__(shoot_position, Vector(car.direction.x * 1000, car.direction.y * 1000), 10)
        self.direction = copy.copy(car.direction)
        self.image = AssetsPort.BULLET
        self.angle = copy.copy(car.angle)
        self.hitbox = Hitbox(0, 0, 15, self)
        self.car = car

        shoot_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'laser.mp3'))
        shoot_sound.set_volume(0.2)
        self.laser_sound = shoot_sound

        self.play_laser_sound()
        
    def play_laser_sound(self):
        self.laser_sound.play()
        
    def physics(self, time: float):
        self.check_left_screen()
        super().physics(time)
        
    def check_left_screen(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (self.position.x > screen_width + 0.03 * screen_width) or (self.position.x < 0 - 0.03 * screen_width) or (self.position.y > screen_height + 0.03 * screen_height) or (self.position.y < 0 - 0.03 * screen_height):
            self.dispose()
            
    def draw(self, win):
        blit_rotate_center(win, self.image, (self.position.x,
                           self.position.y), math.degrees(self.angle))


    def  dispose(self):
        if self in self.car.bullets:
            self.car.bullets.remove(self)
        self.disposed = True
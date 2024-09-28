import math
import os

import pygame

from entities.bullet import Bullet
from entities.hitbox import Hitbox
from entities.object import Object
from entities.vector import Vector
from systems.image_rendering import blit_rotate_center


class Car(Object):
    START_POS = (0, 0)
    DIRECTION_RIGHT = Vector(1, 0)

    def __init__(self, max_vel, rotation_vel, image, screen_width, screen_height, initial_pos, mass):
        super().__init__(initial_pos, Vector(0, 0), mass)
        self.max_vel = max_vel
        self.direction = Vector(1, 0)
        self.rotation_vel = 3.14 * rotation_vel
        self.angle = 0
        self.acceleration = 5
        self.img = image
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hitbox = Hitbox(0, 0, 10, self)
        self.bullets = []  # Inicializa a lista de tiros
        pygame.init()

    def rotate(self, time: float, left=False, right=False):
        if left:
            self.angle += self.rotation_vel * time
        elif right:
            self.angle -= self.rotation_vel * time

        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        self.direction.x = cos_angle * self.DIRECTION_RIGHT.x - \
            sin_angle * self.DIRECTION_RIGHT.y
        self.direction.y = sin_angle * self.DIRECTION_RIGHT.x + \
            cos_angle * self.DIRECTION_RIGHT.y

    def physics(self, time: float):
        if self.vel == 0:
            self.speed = Vector(0, 0)
        elif self.vel < 0:
            self.speed.x = -self.direction.x
            self.speed.y = -self.direction.y
            self.speed.set_module(abs(self.vel))
        else:
            self.speed.x = self.direction.x
            self.speed.y = self.direction.y
            self.speed.set_module(abs(self.vel))

        super().physics(time)
    
        self.check_teleport()

    def move_forward(self, time):
        if self.vel == 0:
           self.play_engine_sound()
        acceleration = (5 if self.vel < 0 else 1) * self.acceleration
        self.vel = min(self.vel + acceleration, self.max_vel)

    def move_backward(self, time):
        if self.vel == 0:
           self.play_engine_sound()
        acceleration = (5 if self.vel > 0 else 1) * self.acceleration
        self.vel = max(self.vel - acceleration, -self.max_vel / 2)

    def reduce_speed(self, time):
        self.vel = max(self.vel - self.acceleration / 2,
                       0) if self.vel > 0 else min(self.vel + self.acceleration / 2, 0)
        
    @staticmethod
    def play_engine_sound():
        engine = pygame.mixer.Sound(os.path.join('assets/sounds', 'car_start.mp3'))
        pygame.mixer.Sound.play(engine)
        
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(self.angle))

    def check_teleport(self):
        if self.position.x > self.screen_width + 0.03 * self.screen_width:
            self.position.x = 0 - 0.03 * self.screen_width
        elif self.position.x < 0 - 0.03 * self.screen_width:
            self.position.x = self.screen_width
        if self.position.y > self.screen_height + 0.03 * self.screen_height:
            self.position.y = 0 - 0.03 * self.screen_height
        elif self.position.y < 0 - 0.03 * self.screen_height:
            self.position.y = self.screen_height

    def shoot(self):
        bullet = Bullet(self)
        self.bullets.append(bullet)
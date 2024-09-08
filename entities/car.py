import math
import os
from components.inputs_port import InputsPort
from entities.hitbox import Hitbox
from entities.object import Object
from entities.vector import Vector
from systems.image_rendering import blit_rotate_center
from enum import Enum
import random
import time as py_time
import pygame

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
        self.hitbox = Hitbox(19, 20, 10, self)
        self.health = 100
        self.is_flashing = False
        self.flash_duration = 8
        self.flash_timer = 0
        pygame.init()
        

    def rotate(self, time: float, left=False, right=False):
        if left:
            self.angle += self.rotation_vel * time
        elif right:
            self.angle -= self.rotation_vel * time

        cosAngle = math.cos(self.angle)
        sinAngle = math.sin(self.angle)

        self.direction.x = cosAngle * self.DIRECTION_RIGHT.x - \
            sinAngle * self.DIRECTION_RIGHT.y
        self.direction.y = sinAngle * self.DIRECTION_RIGHT.x + \
            cosAngle * self.DIRECTION_RIGHT.y

    def physics(self, time: float):
        if self.vel == 0:
            self.speed = Vector(0, 0)
        elif self.vel < 0:
            self.speed.x = -(self.direction.x)
            self.speed.y = -(self.direction.y)
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
        
    def play_engine_sound(self):
        engine = pygame.mixer.Sound(os.path.join('assets/sounds', 'car_start.mp3'))
        pygame.mixer.Sound.play(engine)
        
    def draw(self, win):
        if self.is_flashing: # Se tomou dano
            print("flashing")
            temp_img = self.img.copy()
            red_overlay = pygame.Surface(temp_img.get_size())
            red_overlay.fill((255, 0, 0))
            temp_img.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_MULT)
            blit_rotate_center(win, temp_img, (self.position.x, self.position.y), math.degrees(self.angle))
        else:
            blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(self.angle))
            
    def check_teleport(self):
        if self.position.x > self.screen_width + 0.03 * self.screen_width:
            self.position.x = 0 - 0.03 * self.screen_width
        elif self.position.x < 0 - 0.03 * self.screen_width:
            self.position.x = self.screen_width
        if self.position.y > self.screen_height + 0.03 * self.screen_width:
            self.position.y = 0 - 0.03 * self.screen_width
        elif self.position.y < 0 - 0.03 * self.screen_width:
            self.position.y = self.screen_height

    def takes_damage(self, damage):
        self.health -= damage
        self.is_flashing = True
        self.flash_timer = 0
        
        if self.health <= 0:
            return True  # Retorna que o carro foi explodido
        return False
    
    def update_flash(self, time):
        if self.is_flashing:
            self.flash_timer += time
            print("flash time: "+str(self.flash_timer))
            print("flash duraiton: "+str(self.flash_duration))
            if self.flash_timer >= self.flash_duration:
                self.is_flashing = False
                
    def custom_collision_handling(self):
        self.angle = math.atan2(self.direction.y, self.direction.x)
        self.takes_damage(0)
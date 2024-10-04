import copy

import pygame

from entities.vector import Vector


class Object:
    def __init__(self, position, speed, mass):
        self.initial_position = copy.deepcopy(position)
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário
        self.mass = mass
        self.vel = 0
        self.disposed = False
        self.health = 100
        pygame.init()

    def physics(self, time: float):
        self.position.x += self.speed.x * time
        self.position.y -= self.speed.y * time

    def teleport(self, distance):
        if hasattr(self, "direction"):
            offset = Vector(self.direction.x * distance,
                            self.direction.y * distance)
            self.position = self.position + offset

    def reset(self):
        self.health = 100
        self.position = Vector(self.initial_position.x, self.initial_position.y)
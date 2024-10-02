import pygame

from entities.vector import Vector


class Object:
    def __init__(self, position, speed, mass):
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário
        self.mass = mass
        self.vel = 0
        self.disposed = False
        pygame.init()

    def physics(self, time: float):
        self.position.x += self.speed.x * time
        self.position.y -= self.speed.y * time

    def teleport(self, distance):
        if hasattr(self, "direction"):
            offset = Vector(self.direction.x * distance,
                            self.direction.y * distance)
            self.position = self.position + offset
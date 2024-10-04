import copy
import math
import os

import pygame

from entities.bullet import Bullet
from entities.car import Car
from entities.object import Object
from entities.vector import Vector


class Collision:

    @staticmethod
    def check_collisions(objects):
        num_objects = len(objects)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                if objects[i].hitbox.check_collision(objects[j].hitbox):
                    Collision.handle_collision(objects[i], objects[j])

    @staticmethod
    def handle_collision(obj1, obj2):
        if isinstance(obj1, Bullet) and  isinstance(obj2, Bullet):
            return
        if isinstance(obj1, Bullet) and isinstance(obj2, Car):
            # Tratar colisão específica entre Bullet e Car
            Collision.handle_bullet_car_collision(obj1, obj2)
            return
        elif isinstance(obj1, Car) and isinstance(obj2, Bullet):
            # Tratar colisão específica entre Car e Bullet (inverte a ordem)
            Collision.handle_bullet_car_collision(obj2, obj1)
            return

        engine = pygame.mixer.Sound(
            os.path.join('assets/sounds', 'tuc.mp3'))
        pygame.mixer.Sound.play(engine)
        collision_vector = obj1.position - obj2.position

        teleport_vector = copy.copy(collision_vector)

        teleport_vector.set_module((obj1.hitbox.radius + obj2.hitbox.radius) - collision_vector.module())
        teleport_vector.x = teleport_vector.x * 0.5
        teleport_vector.y = teleport_vector.y * 0.5

        obj1.position += teleport_vector
        obj2.position -= teleport_vector

        qt_mov_obj1 = Vector(obj1.mass * obj1.speed.x, obj1.mass * obj1.speed.y)
        qt_mov_obj2 = Vector(obj2.mass * obj2.speed.x, obj2.mass * obj2.speed.y)

        if abs(qt_mov_obj1.x) + abs(qt_mov_obj1.y) > 0:
            obj2.direction.x = qt_mov_obj1.x / obj2.mass
            obj2.direction.y = qt_mov_obj1.y / obj2.mass
            obj2.vel = obj2.direction.module()
            obj2.direction.normalize()

        if abs(qt_mov_obj2.x) + abs(qt_mov_obj2.y) > 0:
            obj1.direction.x = qt_mov_obj2.x / obj1.mass
            obj1.direction.y = qt_mov_obj2.y / obj1.mass
            obj1.vel = obj1.direction.module()
            obj1.direction.normalize()

        if hasattr(obj1, "angle"):
            obj1.angle = math.atan2(obj1.direction.y, obj1.direction.x)

        if hasattr(obj2, "angle"):
            obj2.angle = math.atan2(obj2.direction.y, obj2.direction.x)

    @staticmethod
    def handle_bullet_car_collision(bullet, car):
        if not (bullet.car == car):
            if car.takes_damage(10):
                bullet.car.kills += 1
            bullet.dispose()

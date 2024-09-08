import copy
import math
import os
import pygame
from entities.vector import Vector
from systems.animations import CollisionAnimation


class Object:
    def __init__(self, position, speed, mass):
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário
        self.mass = mass
        self.vel = 0
        pygame.init()

    def physics(self, time: float):
        self.position.x += self.speed.x * time
        self.position.y -= self.speed.y * time
        
        self.kineticForce = (self.mass * (self.vel * self.vel))/2
        
    def teleport(self, distance):
        if(hasattr(self, "direction")):
            offset = Vector(self.direction.x * distance,
                            self.direction.y * distance)
            self.position = self.position + offset

    @staticmethod
    def check_collisions(game_instance):
        num_objects = len(game_instance.object_list)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                if game_instance.object_list[i].hitbox.check_collision(game_instance.object_list[j].hitbox):
                    Object.handle_collision(game_instance.object_list[i], game_instance.object_list[j])

    @staticmethod
    def handle_collision(obj1, obj2):
        engine = pygame.mixer.Sound(
            os.path.join('assets/sounds', 'tuc.mp3'))
        pygame.mixer.Sound.play(engine)
        collision_vector = obj1.position - obj2.position
        
        # kineticForce = (obj1.kineticForce + obj2.kineticForce) / 2
        # obj1.vel = math.sqrt((2*kineticForce)/obj1.mass)
        # obj2.vel = math.sqrt((2*kineticForce)/obj2.mass)
        # print(str(collision_vector))
    
        teleport_vector = copy.copy(collision_vector) 
        
        teleport_vector.set_module((obj1.hitbox.radius + obj2.hitbox.radius) - collision_vector.module()) 
        teleport_vector.x = teleport_vector.x * 0.5
        teleport_vector.y = teleport_vector.y * 0.5
        
        obj1.position += teleport_vector
        obj2.position -= teleport_vector
        
        qtMovObj1 = Vector(obj1.mass * obj1.speed.x, obj1.mass * obj1.speed.y)
        qtMovObj2 = Vector(obj2.mass * obj2.speed.x, obj2.mass * obj2.speed.y)
        
        if(abs(qtMovObj1.x) + abs(qtMovObj1.y) > 0):
            obj2.direction.x = qtMovObj1.x / obj2.mass
            obj2.direction.y = qtMovObj1.y / obj2.mass
            obj2.vel = obj2.direction.module()
            obj2.direction.normalize()
    
        if(abs(qtMovObj2.x) + abs(qtMovObj2.y) > 0):
            obj1.direction.x = qtMovObj2.x / obj1.mass
            obj1.direction.y = qtMovObj2.y / obj1.mass
            obj1.vel = obj1.direction.module()
            obj1.direction.normalize()
        
        obj1.custom_collision_handling()
        obj2.custom_collision_handling()

        print(f"Colisão detectada entre objeto {obj1} e objeto {obj2}")

    def custom_collision_handling(self):
        return
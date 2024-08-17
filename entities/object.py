import copy
import math
from entities.vector import Vector


class Object:
    def __init__(self, position, speed, mass):
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário
        self.mass = mass
        self.vel = 0

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
    def check_collisions(objects):
        num_objects = len(objects)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                if objects[i].hitbox.check_collision(objects[j].hitbox):
                    Object.handle_collision(objects[i], objects[j])

    @staticmethod
    def handle_collision(obj1, obj2):
        collision_vector = obj1.position - obj2.position
        
        kineticForce = (obj1.kineticForce + obj2.kineticForce) / 2
        obj1.vel = math.sqrt((2*kineticForce)/obj1.mass)
        obj2.vel = math.sqrt((2*kineticForce)/obj2.mass)
        print(str(collision_vector))
        
        teleport_vector = copy.copy(collision_vector) 
        
        teleport_vector.set_module((obj1.hitbox.radius + obj2.hitbox.radius) - collision_vector.module()) 
        teleport_vector.x = teleport_vector.x * 0.5
        teleport_vector.y = teleport_vector.y * 0.5
        
        newDirection = copy.copy(collision_vector)
        newDirection.set_module(1)
        
        if (hasattr(obj1, "direction")):
            obj1.direction.x = newDirection.x
            obj1.direction.y = newDirection.y
            obj1.direction * -1
        
        if (hasattr(obj2,"direction")):
            obj2.direction.x = newDirection.x
            obj2.direction.y = newDirection.y
            
        
        if (hasattr(obj1,"angle")):
            obj1.angle = math.atan2(obj1.direction.y, obj1.direction.x)
            
        if (hasattr(obj2,"angle")):
            obj2.angle = math.atan2(obj2.direction.y, obj2.direction.x)
        
        obj1.position += teleport_vector
        obj2.position -= teleport_vector
        
        
        print(f"Colisão detectada entre objeto {obj1} e objeto {obj2}")

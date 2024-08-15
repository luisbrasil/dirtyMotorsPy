import copy
import math
from entities.vector import Vector


class Object:
    def __init__(self, position, speed, mass, vel):
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário
        self.mass = mass
        self.vel = vel

    def physics(self, time: float):
        self.position.x += self.speed.x * time
        self.position.y -= self.speed.y * time
        
        self.kineticForce = (self.mass * (self.speed * self.speed))/2
        
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
        print(str(collision_vector))
        
        teleport_vector = copy.copy(collision_vector) 
        
        teleport_vector.set_module((obj1.hitbox.radius + obj2.hitbox.radius) - collision_vector.module()) 
        teleport_vector.x = teleport_vector.x * 0.5
        teleport_vector.y = teleport_vector.y * 0.5
        
        # if (hasattr(obj1, "direction")):
        #     obj1.direction.x = collision_vector.x
        #     obj1.direction.y = collision_vector.y
        
        # if (hasattr(obj2,"direction")):
        #     obj2.direction.x = collision_vector.x
        #     obj2.direction.y = collision_vector.y
        #     obj2.direction * -1
        
        # if (hasattr(obj1,"angle")):
        #     obj1.angle = math.atan2(obj1.direction.y, obj1.direction.x)
            
        # if (hasattr(obj2,"angle")):
        #     obj2.angle = math.atan2(obj2.direction.y, obj2.direction.x)
        
        obj1.position += teleport_vector
        obj2.position -= teleport_vector
        
        
        print(f"Colisão detectada entre objeto {obj1} e objeto {obj2}")

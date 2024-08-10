import math
from entities.vector import Vector


class Object:
    def __init__(self, position, speed):
        self.position: Vector = position
        self.speed: Vector = speed
        self.hitbox = None  # Defina a hitbox conforme necessário

    def physics(self, time: float):
        self.position.x += self.speed.x * time
        self.position.y -= self.speed.y * time
        
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
        
        collision_vector.normalize()
        print(str(collision_vector))

        
        if (hasattr(obj1, "direction")):
            obj1.direction = obj1.direction.reflect(collision_vector)
        
        if (hasattr(obj2,"direction")):
            obj2.direction = obj2.direction.reflect(collision_vector)
        
        if (hasattr(obj1,"angle")):
            obj1.angle += math.atan2(obj1.direction.y, obj1.direction.x)
            
        if (hasattr(obj2,"angle")):
            obj2.angle += math.atan2(obj2.direction.y, obj2.direction.x)
        
        teleport_distance = -10
        obj1.teleport(teleport_distance)
        obj2.teleport(teleport_distance)
        
        obj1.vel = 50
        obj2.vel = 50
        
        
        print(f"Colisão detectada entre objeto {obj1} e objeto {obj2}")

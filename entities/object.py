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

    @staticmethod
    def check_collisions(objects):
        num_objects = len(objects)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                if objects[i].hitbox.check_collision(objects[j].hitbox):
                    Object.handle_collision(objects[i], objects[j])

    @staticmethod
    def handle_collision(obj1, obj2):
        
        obj1.direction.x = abs(obj1.speed.x) * -1
        obj1.direction.y = abs(obj1.speed.y) * -1
        obj1.self.angle +=180
        obj1.vel = 50
        obj2.vel = 50
        
        
        print(f"Colisão detectada entre objeto {obj1} e objeto {obj2}")

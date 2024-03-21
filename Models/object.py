from Models.vector import Vector


class Object:
    def __init__(self, position, speed):
        self.position: Vector = position
        self.speed: Vector = speed

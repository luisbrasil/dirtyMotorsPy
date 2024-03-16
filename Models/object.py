from Models.vector import Vector


class Object:
    def __init__(self, point, vector):
        self.point: Vector = point
        self.vector: Vector = vector

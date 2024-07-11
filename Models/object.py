from Models.vector import Vector


class Object:
    def __init__(self, position, speed):
        self.position: Vector = position
        self.speed: Vector = speed
        
    def physics(self, time:float):
        self.position.x += self.speed.x * time
        self.position.y += self.speed.y * time
        #print("Velocidade x =" + str(self.speed.x))
        #print("Velocidade y =" + str(self.speed.y))

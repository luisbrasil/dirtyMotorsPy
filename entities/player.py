from entities.car import Car
from entities.vector import Vector


class Player(Car):
    def __init__(self, max_vel, rotation_vel, image, key_up, key_left, key_down, key_right, screen_width, screen_height):
        super().__init__(max_vel, rotation_vel, image, screen_width, screen_height)
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right

    def handle_input(self, time, keys):
        moved = False
        if keys[self.key_left]:
            self.rotate(time=time, left=True)
        if keys[self.key_right]:
            self.rotate(time=time, right=True)
        if keys[self.key_up]:
            moved = True
            self.move_forward(time)
        if keys[self.key_down]:
            moved = True
            self.move_backward(time)
        if not moved:
            self.reduce_speed(time)

from components.inputs_port import InputsPort
from entities.car import Car


class Player(Car):
    def __init__(self, max_vel, rotation_vel, image, playerNumber, screen_width, screen_height, initial_pos, mass):
        super().__init__(max_vel, rotation_vel, image,
                         screen_width, screen_height, initial_pos, mass)

        if playerNumber == 1:
            self.key_up = InputsPort.KEY_UP
            self.key_down = InputsPort.KEY_DOWN
            self.key_left = InputsPort.KEY_LEFT
            self.key_right = InputsPort.KEY_RIGHT
            self.key_hit = InputsPort.KEY_ONE

        if playerNumber == 2:
            self.key_up = InputsPort.KEY_W
            self.key_down = InputsPort.KEY_S
            self.key_left = InputsPort.KEY_A
            self.key_right = InputsPort.KEY_D
            self.key_hit = InputsPort.KEY_K
            self.angle = 3.14


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
        if keys[self.key_hit]:
            self.shoot()

        if not moved:
            self.reduce_speed(time)

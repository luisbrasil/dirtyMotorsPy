import random
import time as py_time
from entities.car import Car

from entities.vector import Vector


class Bot(Car):
    def __init__(self, max_vel, rotation_vel, image, bot_action_interval, screen_width, screen_height, initial_pos):
        super().__init__(max_vel, rotation_vel, image,
                         screen_width, screen_height, initial_pos)

        self.bot_action_interval = bot_action_interval
        self.last_bot_action_time = py_time.time() 

    def handle_input(self, time):
        current_time = py_time.time()
        if current_time - self.last_bot_action_time >= self.bot_action_interval:
            action = random.choice(['left', 'right', 'forward'])
            if action == 'left':
                self.rotate(time=time, left=True)
            elif action == 'right':
                self.rotate(time=time, right=True)
            elif action == 'forward':
                self.move_forward(time)

            self.last_bot_action_time = current_time

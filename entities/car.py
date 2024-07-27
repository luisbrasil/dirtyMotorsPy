import math
from components.inputs_port import InputsPort
from entities.object import Object
from entities.vector import Vector
from systems.image_rendering import blit_rotate_center
from enum import Enum
import random
import time as py_time

class ControlType(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    BOT = 3

class Car(Object):
    START_POS = (0, 0)
    DIRECTION_RIGHT = Vector(1, 0)

    def __init__(self, max_vel, rotation_vel, image, controlType, screen_width, screen_height):
        super().__init__(Vector(*self.START_POS), Vector(0, 0))
        self.max_vel = max_vel
        self.vel = 0
        self.direction = Vector(1, 0)
        self.rotation_vel = 3.14 * 2
        self.angle = 0
        self.acceleration = 5
        self.img = image
        self.controlType = controlType
        self.last_bot_action_time = py_time.time()
        self.bot_action_interval = 0.005
        self.screen_width = screen_width
        self.screen_height = screen_height

    def rotate(self, time: float, left=False, right=False):
        if left:
            self.angle += self.rotation_vel * time
        elif right:
            self.angle -= self.rotation_vel * time

        cosAngle = math.cos(self.angle)
        sinAngle = math.sin(self.angle)

        self.direction.x = cosAngle * self.DIRECTION_RIGHT.x - \
            sinAngle * self.DIRECTION_RIGHT.y
        self.direction.y = sinAngle * self.DIRECTION_RIGHT.x + \
            cosAngle * self.DIRECTION_RIGHT.y

    def physics(self, time: float):
        if self.vel == 0:
            self.speed = Vector(0, 0)
        elif self.vel < 0:
            self.speed.x = -(self.direction.x)
            self.speed.y = -(self.direction.y)
            self.speed.set_module(abs(self.vel))
        else:
            self.speed.x = self.direction.x
            self.speed.y = self.direction.y
            self.speed.set_module(abs(self.vel))

        super().physics(time)
        self.check_teleport()

    def move_forward(self, time):
        acceleration = (5 if self.vel < 0 else 1) * self.acceleration
        self.vel = min(self.vel + acceleration, self.max_vel)

    def move_backward(self, time):
        acceleration = (5 if self.vel > 0 else 1) * self.acceleration
        self.vel = max(self.vel - acceleration, -self.max_vel / 2)

    def reduce_speed(self, time):
        self.vel = max(self.vel - self.acceleration / 2,
                       0) if self.vel > 0 else min(self.vel + self.acceleration / 2, 0)

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position.x, self.position.y), math.degrees(self.angle))

    def handle_input(self, time, keys):
        moved = False

        if self.controlType == ControlType.PLAYER1:
            if keys[InputsPort.KEY_LEFT]:
                self.rotate(time=time, left=True)
            if keys[InputsPort.KEY_RIGHT]:
                self.rotate(time=time, right=True)
            if keys[InputsPort.KEY_UP]:
                moved = True
                self.move_forward(time)
            if keys[InputsPort.KEY_DOWN]:
                moved = True
                self.move_backward(time)
            if not moved:
                self.reduce_speed(time)
        elif self.controlType == ControlType.PLAYER2:
            if keys[InputsPort.KEY_A]:
                self.rotate(time=time, left=True)
            if keys[InputsPort.KEY_D]:
                self.rotate(time=time, right=True)
            if keys[InputsPort.KEY_W]:
                moved = True
                self.move_forward(time)
            if keys[InputsPort.KEY_S]:
                moved = True
                self.move_backward(time)
            if not moved:
                self.reduce_speed(time)
        elif self.controlType == ControlType.BOT:
            current_time = py_time.time()
            if current_time - self.last_bot_action_time >= self.bot_action_interval:
                action = random.choice(['left', 'right', 'forward', 'backward'])
                if action == 'left':
                    self.rotate(time=time, left=True)
                elif action == 'right':
                    self.rotate(time=time, right=True)
                elif action == 'forward':
                    self.move_forward(time)
                # elif action == 'backward':
                #    self.move_backward(time)

                self.last_bot_action_time = current_time

    def check_teleport(self):
        if self.position.x > self.screen_width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.screen_width
        if self.position.y > self.screen_height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.screen_height


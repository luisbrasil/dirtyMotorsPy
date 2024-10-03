import copy
import os
import sys

import pygame

from components.assets_port import AssetsPort
from components.inputs_port import InputsPort
from entities.bot import Bot
from entities.car import Car
from entities.obstacle import Obstacle
from entities.player import Player
from entities.vector import Vector
from systems.animations import CollisionAnimation
from systems.collision import Collision


class Game:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('assets\paranoid.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.object_list = []
        self.collision_frames = []
        self.load_collision_frames()
        self.collision_animations = []

    def load_collision_frames(self):
        for i in range(1, 7):
            image_path = os.path.join('assets/sprites/animations/explosion', f'frame{i}.png')
            frame = pygame.image.load(image_path)
            self.collision_frames.append(frame)

    def update(self, time):
        for animation in self.collision_animations:
            animation.update()

        self.collision_animations = [anim for anim in self.collision_animations if
                                     anim.current_frame < len(anim.frames) - 1]

        for obj in self.object_list:
            if isinstance(obj, Car):
                obj.update_flash(time)

    def draw(self, surface, time):
        self.update(time)
        for object in self.object_list:
            object.draw(surface)
            # object.hitbox.draw(surface)

        # Desenhar todas as animações de colisão
        for animation in self.collision_animations:
            animation.draw(surface)

    def run(self):
        # Initialize Pygame
        # Constants
        WIDTH, HEIGHT = 800, 600
        FPS = 60

        # Create the Pygame window
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dirty Motors")

        # Initial square position
        player_car = Player(1000, 3, AssetsPort.BLACK_CAR,
                           InputsPort.KEY_UP, InputsPort.KEY_LEFT, InputsPort.KEY_DOWN, InputsPort.KEY_RIGHT, InputsPort.KEY_ONE, WIDTH, HEIGHT, Vector(0, 0),100)
        player_car2 = Player(1000, 3, AssetsPort.GREEN_CAR,
                            InputsPort.KEY_W, InputsPort.KEY_A, InputsPort.KEY_S, InputsPort.KEY_D, InputsPort.KEY_Q, WIDTH, HEIGHT, Vector(100, 100),100)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, WIDTH, HEIGHT, Vector(200, 200), 1)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05,
                   WIDTH, HEIGHT,  Vector(300, 300), 1)
        rock_obstacle = Obstacle(50000,AssetsPort.PREDA)

        self.object_list.append(player_car)
        self.object_list.append(player_car2)

        # Set up clock to control the frame rate
        clock = pygame.time.Clock()

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle key events for moving the square
            keys = pygame.key.get_pressed()
            time = clock.tick(60) / 1000
            
            # Load the background image
            background_image = pygame.image.load(
                "assets/sprites/PokeArena.png")

            # Scale the background image to fit the screen size
            background_image = pygame.transform.scale(
                background_image, (WIDTH, HEIGHT))

            # Renderize the background image
            screen.blit(background_image, (0, 0))
            
            for objeto in self.object_list:
                if type(objeto) is Bot:
                    objeto.handle_input(time)
                elif type(objeto) is Player:
                    objeto.handle_input(time, keys)
                    for bullet in objeto.bullets:
                        if bullet not in self.object_list:
                            self.object_list.append(bullet)

            Collision.check_collisions(self.object_list)

            for objeto in self.object_list:
                if objeto.disposed:
                    self.object_list.remove(objeto)
                else:
                    objeto.physics(time)
                    if objeto.health <= 0:
                        collision_position = copy.deepcopy(objeto.position)
                        self.collision_animations.append(CollisionAnimation(self.collision_frames, collision_position))
                        objeto.reset()
            
            
            self.draw(screen, time)
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)
            
        

        # Done! Time to quit.
        pygame.quit()
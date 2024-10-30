import copy
import os
import sys
from time import sleep

import pygame

from components.assets_port import AssetsPort
from entities.bot import Bot
from entities.car import Car
from entities.obstacle import Obstacle
from entities.player import Player
from entities.vector import Vector
from systems.animations import CollisionAnimation
from systems.collision import Collision


class Game:
    WIDTH = 1366
    HEIGHT = 768

    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('assets/paranoid.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.object_list = []
        self.collision_frames = []
        self.load_collision_frames()
        self.collision_animations = []
        self.font = pygame.font.Font(None, 36)

        self.explosion_time = None

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
                obj.update_car(time)

    def draw(self, surface, time):
        self.update(time)
        for object in self.object_list:
            object.draw(surface)

        for animation in self.collision_animations:
            animation.draw(surface)

        player1_kills_text = self.font.render(f'Player 1 Kills: {self.object_list[0].kills}', True, (255, 0, 0))
        player2_kills_text = self.font.render(f'Player 2 Kills: {self.object_list[1].kills}', True, (0, 255, 0))

        surface.blit(player1_kills_text, (10, 10))
        surface.blit(player2_kills_text, (1100, 10))

    def run(self):
        FPS = 60
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dirty Motors")

        player_car = Player(500, 3, AssetsPort.RED_CAR, 1, self.WIDTH, self.HEIGHT, Vector(200, 375), 100)
        player_car2 = Player(500, 3, AssetsPort.GREEN_CAR, 2, self.WIDTH, self.HEIGHT, Vector(1150, 375), 100)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, self.WIDTH, self.HEIGHT, Vector(200, 200), 1)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05, self.WIDTH, self.HEIGHT, Vector(300, 300), 1)
        rock_obstacle = Obstacle(50000, AssetsPort.PREDA)

        self.object_list.append(player_car)
        self.object_list.append(player_car2)

        clock = pygame.time.Clock()
        gets_hammered_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'gets-hammered.mp3'))
        gets_hammered_sound.set_volume(2)

        explosion_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'explosion.mp3'))
        explosion_sound.set_volume(0.2)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            time = clock.tick(60) / 1000

            background_image = pygame.image.load("assets/sprites/PokeArena.png")
            background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
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
                        explosion_sound.play()
                        self.explosion_time = pygame.time.get_ticks()

                        collision_position = copy.deepcopy(objeto.position)
                        self.collision_animations.append(CollisionAnimation(self.collision_frames, collision_position))
                        objeto.reset()

            if self.explosion_time and pygame.time.get_ticks() - self.explosion_time >= 500:
                gets_hammered_sound.play()
                self.explosion_time = None
            self.draw(screen, time)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

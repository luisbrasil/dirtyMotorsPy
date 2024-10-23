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
        pygame.mixer.music.load('assets\paranoid.mp3')
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
            # object.hitbox.draw(surface)

        # Desenhar todas as animações de colisão
        for animation in self.collision_animations:
            animation.draw(surface)

        player1_kills_text = self.font.render(f'Player 1 Kills: {self.object_list[0].kills}', True, (255, 0, 0))
        player2_kills_text = self.font.render(f'Player 2 Kills: {self.object_list[1].kills}', True, (0, 255, 0))

        # Blit the kills text onto the surface at the top of the screen
        surface.blit(player1_kills_text, (10, 10))  # Player 1 kills at top-left
        surface.blit(player2_kills_text, (600, 10))  # Player 2 kills below Player 1 kills

    def run(self):
        # Initialize Pygame
        # Constants
        FPS = 60

        # Create the Pygame window
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dirty Motors")
        
        self.show_start_menu(screen)

        # Initial square position
        player_car = Player(500, 3, AssetsPort.RED_CAR, 1, self.WIDTH, self.HEIGHT, Vector(100, 300), 100)
        player_car2 = Player(500, 3, AssetsPort.GREEN_CAR, 2, self.WIDTH, self.HEIGHT, Vector(700, 300), 100)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, self.WIDTH, self.HEIGHT, Vector(200, 200), 1)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05,
                   self.WIDTH, self.HEIGHT, Vector(300, 300), 1)
        rock_obstacle = Obstacle(50000, AssetsPort.PREDA)

        self.object_list.append(player_car)
        self.object_list.append(player_car2)

        # Set up clock to control the frame rate
        clock = pygame.time.Clock()

        gets_hammered_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'gets-hammered.mp3'))
        gets_hammered_sound.set_volume(2)

        explosion_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'explosion.mp3'))
        explosion_sound.set_volume(0.2)

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
                background_image, (self.WIDTH, self.HEIGHT))

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
                        explosion_sound.play()
                        self.explosion_time = pygame.time.get_ticks()

                        collision_position = copy.deepcopy(objeto.position)
                        self.collision_animations.append(CollisionAnimation(self.collision_frames, collision_position))
                        objeto.reset()

            if self.explosion_time and pygame.time.get_ticks() - self.explosion_time >= 500:
                gets_hammered_sound.play()
                self.explosion_time = None
            self.draw(screen, time)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()
        
    def show_start_menu(self, screen):
        background_image = pygame.image.load("assets/sprites/menu-inicial.jpg")
        background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))

        menu_options = ["Start", "Exit"]
        selected_option = 0

        while True:
            # Renderiza o fundo do menu
            screen.blit(background_image, (0, 0))

            # Desenha as opções do menu
            for i, option in enumerate(menu_options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                text_surface = self.font.render(option, True, color)
                screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2, 400 + i * 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # "Start" selecionado
                            return  # Sai da função e inicia o jogo
                        elif selected_option == 1:  # "Exit" selecionado
                            pygame.quit()
                            sys.exit()
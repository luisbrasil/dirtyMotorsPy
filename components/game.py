import copy
import json
import os
import sys

import pygame

from components.assets_port import AssetsPort
from entities.bot import Bot
from entities.car import Car
from entities.player import Player
from entities.vector import Vector
from systems.animations import CollisionAnimation
from systems.collision import Collision


class Game:
    WIDTH = 1366
    HEIGHT = 768
    GAME_DURATION = 300  # duração do jogo em segundos (5 minutos)

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
        self.start_time = None

    def load_collision_frames(self):
        for i in range(1, 7):
            image_path = os.path.join('assets/sprites/animations/explosion', f'frame{i}.png')
            frame = pygame.image.load(image_path)
            self.collision_frames.append(frame)

    def calculate_time_remaining(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_left = max(0, self.GAME_DURATION - int(elapsed_time))
        minutes = time_left // 60
        seconds = time_left % 60
        return f"{minutes:02}:{seconds:02}"

    def update(self, time):
        for animation in self.collision_animations:
            animation.update()
        self.collision_animations = [anim for anim in self.collision_animations if anim.current_frame < len(anim.frames) - 1]
        for obj in self.object_list:
            if isinstance(obj, Car):
                obj.update_car(time)

    def draw(self, surface, time):
        self.update(time)
        for object in self.object_list:
            object.draw(surface)
        for animation in self.collision_animations:
            animation.draw(surface)

        # Exibir contador de tempo
        time_text = self.calculate_time_remaining()
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surface, (self.WIDTH // 2 - time_surface.get_width() // 2, 10))

        # Exibir contagem de eliminações dos jogadores
        player1_kills_text = self.font.render(f'Player 1 Kills: {self.object_list[0].kills}', True, (255, 0, 0))
        player2_kills_text = self.font.render(f'Player 2 Kills: {self.object_list[1].kills}', True, (0, 255, 0))
        surface.blit(player1_kills_text, (10, 10))
        surface.blit(player2_kills_text, (1100, 10))

    def save_score(self, player1_name, player2_name, player1_kills, player2_kills):
        score_data = {
            "Player 1": {"name": player1_name, "kills": player1_kills},
            "Player 2": {"name": player2_name, "kills": player2_kills}
        }
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        scores.append(score_data)

        with open("scores.json", "w") as file:
            json.dump(scores, file, indent=4)

    def get_player_name(self, surface, prompt):
        name = ""
        input_active = True
        while input_active:
            surface.fill((0, 0, 0))
            prompt_surface = self.font.render(prompt, True, (255, 255, 255))
            name_surface = self.font.render(name, True, (255, 255, 255))
            surface.blit(prompt_surface, (self.WIDTH // 2 - prompt_surface.get_width() // 2, 200))
            surface.blit(name_surface, (self.WIDTH // 2 - name_surface.get_width() // 2, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        return name

    def show_results_screen(self, surface):
        player1_kills = self.object_list[0].kills
        player2_kills = self.object_list[1].kills
        player1_name = self.get_player_name(surface, "Enter name for Player 1:")
        player2_name = self.get_player_name(surface, "Enter name for Player 2:")

        # Salvar pontuação
        self.save_score(player1_name, player2_name, player1_kills, player2_kills)

        # Exibir resultados
        surface.fill((0, 0, 0))
        results_text = [
            f'{player1_name} Kills: {player1_kills}',
            f'{player2_name} Kills: {player2_kills}',
            "",
            "Press ESC to return to the main menu"
        ]
        for i, line in enumerate(results_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            surface.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 40))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def run(self):
        FPS = 60
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dirty Motors")

        # Instanciando os jogadores e bots
        player_car = Player(500, 3, AssetsPort.RED_CAR, 1, self.WIDTH, self.HEIGHT, Vector(200, 375), 100)
        player_car2 = Player(500, 3, AssetsPort.GREEN_CAR, 2, self.WIDTH, self.HEIGHT, Vector(1150, 375), 100)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, self.WIDTH, self.HEIGHT, Vector(200, 200), 1)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05, self.WIDTH, self.HEIGHT, Vector(300, 300), 1)
        self.object_list.extend([player_car, player_car2])

        # Tempo inicial
        self.start_time = pygame.time.get_ticks()

        clock = pygame.time.Clock()
        gets_hammered_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'gets-hammered.mp3'))
        gets_hammered_sound.set_volume(2)
        explosion_sound = pygame.mixer.Sound(os.path.join('assets/sounds', 'explosion.mp3'))
        explosion_sound.set_volume(0.2)

        # Loop principal do jogo
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Verifica se o tempo de jogo acabou
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed_time >= self.GAME_DURATION:
                self.show_results_screen(screen)
                return

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

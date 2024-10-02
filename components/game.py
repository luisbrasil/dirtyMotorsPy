import sys

import pygame

from components.assets_port import AssetsPort
from components.inputs_port import InputsPort
from entities.bot import Bot
from entities.obstacle import Obstacle
from entities.player import Player
from entities.vector import Vector
from systems.collision import Collision


class Game:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('assets\paranoid.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
    

    @staticmethod
    def run():
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
        
        object_list = [player_car, player_car2]

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
            
            for objeto in object_list:
                if type(objeto) is Bot:
                    objeto.handle_input(time)
                elif type(objeto) is Player:
                    objeto.handle_input(time, keys)
                    for bullet in objeto.bullets:
                        if bullet not in object_list:
                            object_list.append(bullet)

            Collision.check_collisions(object_list)

            for objeto in object_list:
                if objeto.disposed:
                    object_list.remove(objeto)
                else:
                    objeto.physics(time)
            
            
            for objeto in object_list:
                objeto.draw(screen)
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)
            
        

        # Done! Time to quit.
        pygame.quit()
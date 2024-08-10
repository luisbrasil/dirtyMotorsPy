import sys
import pygame
from components.assets_port import AssetsPort
from components.inputs_port import InputsPort
from entities.bot import Bot
from entities.object import Object
from entities.obstacle import Obstacle
from entities.player import Player
from entities.vector import Vector
from systems.image_rendering import scale_image

class Game:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('assets\Thunderstruck.mp3')
        pygame.mixer.music.play()
    
    
    def run(self):
        # Initialize Pygame
        # Constants
        WIDTH, HEIGHT = 800, 600
        FPS = 60

        # Create the Pygame window
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dirty Motors")

        # Initial square position
        playerCar = Player(1000, 3, AssetsPort.BLACK_CAR,
                           InputsPort.KEY_UP, InputsPort.KEY_LEFT, InputsPort.KEY_DOWN, InputsPort.KEY_RIGHT, WIDTH, HEIGHT, Vector(0, 0))
        playerCar2 = Player(1000, 3, AssetsPort.GREEN_CAR,
                            InputsPort.KEY_W, InputsPort.KEY_A, InputsPort.KEY_S, InputsPort.KEY_D, WIDTH, HEIGHT, Vector(100, 100))
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, WIDTH, HEIGHT, Vector(200, 200))
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05,
                   WIDTH, HEIGHT,  Vector(300, 300))
        rockObstacle = Obstacle(AssetsPort.PREDA)
        
        object_list = [playerCar, playerCar2]

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
                "assets/sprites/RacingTrack.png")

            # Scale the background image to fit the screen size
            background_image = pygame.transform.scale(
                background_image, (WIDTH, HEIGHT))

            # Renderize the background image
            screen.blit(background_image, (0, 0))
            
            for object in object_list:
                if type(object) is Bot:
                    object.handle_input(time)
                elif type(object) is Player:
                    object.handle_input(time, keys)
            
            Object.check_collisions(object_list)
            
            for object in object_list:
                object.physics(time)
            
            
            for object in object_list:
                object.draw(screen) 
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()
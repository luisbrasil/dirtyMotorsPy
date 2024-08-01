import sys
import pygame
from components.assets_port import AssetsPort
from components.inputs_port import InputsPort
from entities.bot import Bot
from entities.obstacle import Obstacle
from entities.player import Player
from systems.image_rendering import scale_image

class Game:
    
    def __init__(self):
        pygame.init()
    
    
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
                        InputsPort.KEY_UP, InputsPort.KEY_LEFT, InputsPort.KEY_DOWN, InputsPort.KEY_RIGHT, WIDTH, HEIGHT)
        playerCar2 = Player(1000, 3, AssetsPort.GREEN_CAR,
                         InputsPort.KEY_W, InputsPort.KEY_A, InputsPort.KEY_S, InputsPort.KEY_D, WIDTH, HEIGHT)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, WIDTH, HEIGHT)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05, WIDTH, HEIGHT)
        rockObstacle = Obstacle(AssetsPort.PREDA)
        
        object_list = [playerCar, playerCar2, bot, bot2, rockObstacle]

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
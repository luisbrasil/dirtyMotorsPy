import sys
import pygame
from components.assets_port import AssetsPort
from entities.obstacle import Obstacle
from entities.car import Car
from entities.car import ControlType
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
        playerCar = Car(1000, 100, AssetsPort.BLACK_CAR, ControlType.PLAYER1)
        playerCar2 = Car(1000, 100, AssetsPort.GREEN_CAR, ControlType.PLAYER2)
        bot = Car(1000, 100, AssetsPort.PINK_CAR, ControlType.BOT)
        bot2 = Car(1000, 100, AssetsPort.BLUE_CAR, ControlType.BOT)
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
            
            playerCar.handle_input(time,keys)
            for object in object_list:
                object.physics(time)

            playerCar2.handle_input(time, keys)
            for object in object_list:
                object.physics(time)
            
            bot.handle_input(time, keys)
            for object in object_list:
                object.physics(time)
                
            bot2.handle_input(time, keys)
            for object in object_list:
                object.physics(time)
            
            # Load the background image
            background_image = pygame.image.load("assets/sprites/RacingTrack.png")

            # Scale the background image to fit the screen size
            background_image = pygame.transform.scale(
                background_image, (WIDTH, HEIGHT))

            # Renderize the background image
            screen.blit(background_image, (0, 0))

            playerCar.draw(screen)
            playerCar2.draw(screen)
            bot.draw(screen)
            bot2.draw(screen)
            rockObstacle.draw(screen)
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()
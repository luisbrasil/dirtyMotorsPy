import sys
import pygame
from components.assets_port import AssetsPort
from entities.obstacle import Obstacle
from entities.car import Car
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
        playerCar = Car(1000, 10, AssetsPort.BLACK_CAR)
        rockObstacle = Obstacle(AssetsPort.PREDA)
        
        object_list = [playerCar, rockObstacle]

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

            # Load the background image
            background_image = pygame.image.load("assets/sprites/RacingTrack.png")

            # Scale the background image to fit the screen size
            background_image = pygame.transform.scale(
                background_image, (WIDTH, HEIGHT))

            # Renderize the background image
            screen.blit(background_image, (0, 0))

            playerCar.draw(screen)
            rockObstacle.draw(screen)
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()
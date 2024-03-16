import pygame
import sys
from Models.car import Car
from utils import scale_image

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 50
FPS = 60

# Colors 
BLACK_CAR = scale_image(pygame.image.load("sprites/BlackOut.png"), 0.55)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")

# Initial square position
playerCar = Car(10,1)
square_x = WIDTH // 2 - SQUARE_SIZE // 2
square_y = HEIGHT // 2 - SQUARE_SIZE // 2

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
    if keys[pygame.K_LEFT]:
        playerCar.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        playerCar.rotate(right=True)
    if keys[pygame.K_UP]:
        playerCar.point.x -= 5
        pass
    if keys[pygame.K_DOWN]:
        playerCar.point.x += 5
        pass

     # Load the background image
    background_image = pygame.image.load("sprites/RacingTrack.png")

    # Scale the background image to fit the screen size
    background_image = pygame.transform.scale(
        background_image, (WIDTH, HEIGHT))

    # Renderize the background image
    screen.blit(background_image, (0, 0))

    # Draw the square
    car_image = BLACK_CAR
    rotated_car = pygame.transform.rotate(car_image, playerCar.angle)
    screen.blit(rotated_car, (playerCar.point.x, playerCar.point.y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()
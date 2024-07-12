import sys
import pygame
from models.car import Car
from utils.image_rendering import scale_image

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 50
FPS = 60

# Colors 
BLACK_CAR = scale_image(pygame.image.load("assets/sprites/BlackOut.png"), 0.55)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")

# Initial square position
playerCar = Car(1000, 10, BLACK_CAR)
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
    moved = False
    time = clock.tick(60) / 1000
    
    if keys[pygame.K_LEFT]:
        playerCar.rotate(time=time,left=True)
    if keys[pygame.K_RIGHT]:
        playerCar.rotate(time=time,right=True)
    if keys[pygame.K_UP]:
        moved = True
        playerCar.move_forward(time)
    if keys[pygame.K_DOWN]:
        moved = True
        playerCar.move_backward(time)
    
    if not moved:
        playerCar.reduce_speed(time)

    playerCar.physics(time)

     # Load the background image
    background_image = pygame.image.load("assets/sprites/RacingTrack.png")

    # Scale the background image to fit the screen size
    background_image = pygame.transform.scale(
        background_image, (WIDTH, HEIGHT))

    # Renderize the background image
    screen.blit(background_image, (0, 0))

    playerCar.draw(screen)

    #Tratar o eixo de rotação sendo o eixo central
    #Pegar height e width do carro 
    #Alguma maneira de reutilizar o sprite antigo sem ter que gerar um novo sprit o tempo todo
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")

# Initial square position
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
        square_x -= 5
    if keys[pygame.K_RIGHT]:
        square_x += 5
    if keys[pygame.K_UP]:
        square_y -= 5
    if keys[pygame.K_DOWN]:
        square_y += 5

    # Fill the screen with the background color
    screen.fill(WHITE)

    # Draw the square
    pygame.draw.rect(
        screen, RED, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()
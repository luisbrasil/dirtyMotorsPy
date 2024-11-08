import pygame
from systems.image_rendering import scale_image


class AssetsPort:
    BLACK_CAR = scale_image(pygame.image.load("assets/sprites/BlackOut.png"), 0.55)
    GREEN_CAR = scale_image(pygame.image.load(
        "assets/sprites/GreenStrip.png"), 0.55)
    BLUE_CAR = scale_image(pygame.image.load(
        "assets/sprites/BlueStrip.png"), 0.55)
    PINK_CAR = scale_image(pygame.image.load(
        "assets/sprites/PinkStrip.png"), 0.55)
    RED_CAR = scale_image(pygame.image.load(
        "assets/sprites/RedStrip.png"), 0.55)
    PREDA = scale_image(pygame.image.load("assets/sprites/preda.png"), 0.20)
    BULLET = scale_image(pygame.image.load("assets/sprites/bullet.png"), 0.06)
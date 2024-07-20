import pygame
from utils.image_rendering import scale_image


class AssetsPort:
    BLACK_CAR = scale_image(pygame.image.load("assets/sprites/BlackOut.png"), 0.55)
    PREDA = scale_image(pygame.image.load("assets/sprites/preda.png"), 0.20)
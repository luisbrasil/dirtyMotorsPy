import json
import sys
import os
from entities.car import Car
from systems.animations import CollisionAnimation
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
        pygame.mixer.music.load('assets\paranoid.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.object_list = []
        self.collision_frames = []
        self.load_collision_frames()
        self.collision_animations = []
    
    def load_collision_frames(self):
        for i in range(1, 7):
            image_path = os.path.join('assets/sprites/animated/explosion', f'frame{i}.png')
            frame = pygame.image.load(image_path)
            self.collision_frames.append(frame)
            
    def update(self, time):
        # Atualizar todas as animações de colisão
        for animation in self.collision_animations:
            animation.update()
            
        # Remover animações concluídas
        self.collision_animations = [anim for anim in self.collision_animations if anim.current_frame < len(anim.frames) - 1]
        
        for obj in self.object_list:
            if isinstance(obj, Car):
                obj.update_flash(time)
            
    def draw(self, surface, time):
        self.update(time)
        for object in self.object_list:
            object.draw(surface)
        
        # Desenhar todas as animações de colisão
        for animation in self.collision_animations:
            animation.draw(surface)

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
                           InputsPort.KEY_UP, InputsPort.KEY_LEFT, InputsPort.KEY_DOWN, InputsPort.KEY_RIGHT, InputsPort.KEY_ONE, WIDTH, HEIGHT, Vector(0, 0),100)
        playerCar2 = Player(1000, 3, AssetsPort.GREEN_CAR,
                            InputsPort.KEY_W, InputsPort.KEY_A, InputsPort.KEY_S, InputsPort.KEY_D, InputsPort.KEY_Q, WIDTH, HEIGHT, Vector(100, 100),100)
        bot = Bot(1000, 2, AssetsPort.PINK_CAR, 0.05, WIDTH, HEIGHT, Vector(200, 200), 1)
        bot2 = Bot(1000, 2, AssetsPort.BLUE_CAR, 0.05,
                   WIDTH, HEIGHT,  Vector(300, 300), 1)
        rockObstacle = Obstacle(50000,AssetsPort.PREDA)
        
        self.object_list.append(playerCar)
        self.object_list.append(playerCar2)

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
            
            for object in self.object_list:
                if type(object) is Bot:
                    object.handle_input(time)
                elif type(object) is Player:
                    object.handle_input(time, keys)
            
            Object.check_collisions(self)
            
            for object in self.object_list:
                object.physics(time)
                if object.health <= 0:
                   #self.collision_animations.append(CollisionAnimation(self.collision_frames, object.position))
                    self.object_list.remove(object)

            self.draw(screen, time)
            
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()
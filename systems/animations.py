import pygame

from systems.image_rendering import blit_rotate_center


class CollisionAnimation:
    def __init__(self, frames, position):
        self.frames = frames
        self.position = position
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milliseconds between frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
            self.last_update = now

    def draw(self, surface):
        blit_rotate_center(surface, self.frames[self.current_frame], (self.position.x, self.position.y), 0)

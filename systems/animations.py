import pygame

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
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.position)

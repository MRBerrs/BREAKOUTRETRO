import pygame
from setting import *

class Ball:
    def __init__(self, x, y, size=18, dx=5, dy=-5):
        self.x, self.y = x, y
        self.size = size
        self.dx, self.dy = dx, dy
        self.original_size = size

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= SETTINGS["screen_width"] - self.size:
            self.dx = -self.dx

        if self.y <= 0:
            self.dy = -self.dy

    def enlarge(self):
        self.size = min(self.size + 5, 40)

    def reset(self):
        self.size = self.original_size

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))

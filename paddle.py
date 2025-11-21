import pygame
from setting import *

class Paddle:
    def __init__(self, x, y, width=120, height=10, speed=10):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.speed = speed
        self.original_width = width
        self.original_height = height

    def update(self):
        mouse_x, _ = pygame.mouse.get_pos()
        target = mouse_x - self.width // 2
        self.x += (target - self.x) * 0.4
        self.x = max(0, min(SETTINGS["screen_width"] - self.width, self.x))

    def enlarge(self):
        self.width = min(self.width + 30, 250)

    def shrink(self):
        self.width = max(self.width - 30, 60)

    def reset(self):
        self.width = self.original_width

    def draw(self, screen):
        pygame.draw.rect(screen, RETRO_GREEN, (self.x, self.y, self.width, self.height))

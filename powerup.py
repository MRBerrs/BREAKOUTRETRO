import pygame
from setting import *

class PowerUp:
    def __init__(self, x, y, ptype, img):
        self.x, self.y = x, y
        self.size = 28
        self.type = ptype
        self.image = img
        self.speed = 3
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y > SETTINGS["screen_height"]:
            self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))

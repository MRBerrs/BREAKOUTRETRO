import pygame
from setting import *

class PowerUp:
    def __init__(self, x, y, ptype, img=None):
        self.x = x
        self.y = y
        self.size = 28
        self.type = ptype
        self.speed = 3
        self.active = True

        # fallback image jika None
        if img is None:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(RETRO_YELLOW)
        else:
            self.image = img

    def update(self):
        self.y += self.speed
        if self.y > SETTINGS["screen_height"]:
            self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))

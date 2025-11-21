import pygame
from setting import *
from game import Game
from menu import main_menu



if __name__ == "__main__":
    screen = pygame.display.set_mode((SETTINGS["screen_width"], SETTINGS["screen_height"]))
    pygame.display.set_caption("Breakout Retro OOP Edition")
    main_menu(screen)
    
    result = main_menu(screen)

if result == "Start Game":
    game = Game(screen)
    game.run()

elif result == "Exit":
    pygame.quit(); exit()
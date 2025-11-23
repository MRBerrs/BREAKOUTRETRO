import pygame
from game import Game
from setting import *

pygame.init()
screen = pygame.display.set_mode((SETTINGS["screen_width"], SETTINGS["screen_height"]))
pygame.display.set_caption("Retro Breakout")

font_title = pygame.font.Font(None, 90)
font_btn = pygame.font.Font(None, 50)

def draw_button(text, x, y):
    surf = font_btn.render(text, True, WHITE)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)
    return rect

def main_menu():
    pygame.mouse.set_visible(True)

    while True:
        screen.fill(BLACK)

        # Title
        title = font_title.render("BREAKOUT RETRO", True, RETRO_YELLOW)
        rect_title = title.get_rect(center=(SETTINGS["screen_width"]//2, 150))
        screen.blit(title, rect_title)

        # Buttons
        start_btn = draw_button("Start Game", SETTINGS["screen_width"]//2, 300)
        settings_btn = draw_button("Settings", SETTINGS["screen_width"]//2, 380)
        exit_btn = draw_button("Exit", SETTINGS["screen_width"]//2, 460)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if start_btn.collidepoint(mx, my):
                    game = Game(screen)
                    game.run()  #To the game
                elif settings_btn.collidepoint(mx, my):
                    print("Settings nanti aja cok")
                elif exit_btn.collidepoint(mx, my):
                    pygame.quit(); exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

#Menu
main_menu()
waiting = False
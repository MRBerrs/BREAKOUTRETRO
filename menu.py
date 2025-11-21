import pygame
from setting import *
from game import Game

def main_menu(screen):
    clock = pygame.time.Clock()
    options = ["Start Game", "Exit"]
    selected = 0

    font_title = pygame.font.Font(None, 60)
    font_opt = pygame.font.Font(None, 40)

    while True:
        screen.fill(BLACK)

        # Title
        title = font_title.render("BREAKOUT RETRO", True, RETRO_YELLOW)
        screen.blit(title, (SETTINGS["screen_width"]//2 - title.get_width()//2, 160))

        # Generate option rect list
        option_rects = []
        for i, text in enumerate(options):
            color = RETRO_GREEN if i == selected else WHITE
            rendered = font_opt.render(text, True, color)
            rect = rendered.get_rect(center=(SETTINGS["screen_width"]//2, 300 + i*60))
            option_rects.append(rect)
            screen.blit(rendered, rect)

        pygame.display.flip()
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

            # Keyboard
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if selected == 0:
                        return "start"
                    elif selected == 1:
                        pygame.quit(); exit()

            # MOUSE MOVE
            elif e.type == pygame.MOUSEMOTION:
                mouse_pos = e.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selected = i

            # MOUSE CLICK
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:  # left click
                    mouse_pos = e.pos
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            if i == 0:
                                return "start"
                            elif i == 1:
                                pygame.quit(); exit()

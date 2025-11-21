import pygame, random, time
from setting import *
from paddle import Paddle
from ball import Ball
from block import Block
from powerup import PowerUp

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.paddle = Paddle(SETTINGS["screen_width"]//2 - 60, SETTINGS["screen_height"] - 60)
        self.balls = [Ball(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2)]
        self.blocks = []
        self.powerups = []
        self.active_powers = []
        self.create_blocks()

    def create_blocks(self):
        colors = [RETRO_RED, RETRO_ORANGE, RETRO_YELLOW, RETRO_BLUE, RETRO_PURPLE]
        for row in range(5):
            for col in range(10):
                x = col * 70 + 40
                y = row * 25 + 60
                self.blocks.append(Block(x, y, 60, 20, colors[row]))

    def update(self):
        self.paddle.update()

        for ball in self.balls:
            ball.update()

        self.check_collision()

        for p in self.powerups[:]:
            p.update()
            if not p.active:
                self.powerups.remove(p)

    def check_collision(self):
        for ball in self.balls[:]:
            if ball.y > SETTINGS["screen_height"]:
                self.balls.remove(ball)
                continue

            # Paddle
            if self.paddle.y <= ball.y + ball.size <= self.paddle.y + self.paddle.height:
                if self.paddle.x <= ball.x <= self.paddle.x + self.paddle.width:
                    rel = (ball.x - self.paddle.x) / self.paddle.width
                    ball.dx = (rel - 0.5) * 10
                    ball.dy = -abs(ball.dy)

            # Blocks
            for block in self.blocks:
                if not block.destroyed:
                    if block.x <= ball.x <= block.x + block.width and \
                       block.y <= ball.y <= block.y + block.height:
                        ball.dy *= -1
                        block.destroyed = True

                        if random.random() < 0.3:
                            self.powerups.append(
                                PowerUp(block.x + block.width//2, block.y, "extra", None)
                            )

    def draw(self):
        self.paddle.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        for b in self.blocks:
            b.draw(self.screen)
        for p in self.powerups:
            p.draw(self.screen)


    def run(self):
        pygame.mouse.set_visible(False)
        running = True
        start_time = time.time()

        # Delay 5 detik sebelum game mulai
        while time.time() - start_time < 5:
            self.screen.fill(BLACK)

            countdown = 5 - int(time.time() - start_time)
            font = pygame.font.Font(None, 80)
            text = font.render(str(countdown), True, RETRO_YELLOW)
            rect = text.get_rect(center=(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2))
            self.screen.blit(text, rect)

            pygame.display.flip()
            self.clock.tick(60)

        # Main game loop
        while running:
            self.screen.fill(BLACK)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

            # If all balls lost → game over
            if len(self.balls) == 0:
                running = False

        # Game over popup
        self.game_over_popup()
    def game_over_popup(self):
        font = pygame.font.Font(None, 60)
        text = font.render("GAME OVER", True, RETRO_RED)
        rect = text.get_rect(center=(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2 - 30))

        subfont = pygame.font.Font(None, 40)
        subtext = subfont.render("Press any key to return to menu", True, WHITE)
        subrect = subtext.get_rect(center=(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2 + 30))

        waiting = True
        while waiting:
            self.screen.fill(BLACK)
            self.screen.blit(text, rect)
            self.screen.blit(subtext, subrect)
            pygame.display.flip()
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                elif e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    
        self.reset()
        pygame.mouse.set_visible(True)
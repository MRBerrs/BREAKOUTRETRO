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
        self.paddle = Paddle(
            SETTINGS["screen_width"]//2 - 60,
            SETTINGS["screen_height"] - 60
        )
        self.balls = [Ball(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2)]
        self.blocks = []
        self.powerups = []
        self.active_powerups = []
        self.create_blocks()

    def create_blocks(self):
        colors = [RETRO_RED, RETRO_ORANGE, RETRO_YELLOW, RETRO_BLUE, RETRO_PURPLE]
        for row in range(5):
            for col in range(10):
                x = col * 70 + 40
                y = row * 25 + 60
                self.blocks.append(Block(x, y, 60, 20, colors[row]))

    # ==========================================================
    def update(self):
        self.paddle.update()

        # POWERUP FALL + COLLISION
        for p in self.powerups:
            p.update()

            if not p.active:
                continue

            paddle_rect = pygame.Rect(self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height)
            power_rect = pygame.Rect(p.x - p.size//2, p.y - p.size//2, p.size, p.size)

            if paddle_rect.colliderect(power_rect):
                p.active = False
                self.apply_powerup(p.type)
                duration = 5
                self.active_powerups.append({
                "type": p.type,
                "end_time": time.time() + duration
            })
                
                # === CHECK POWERUP EXPIRE ===
            now = time.time()
            for pw in self.active_powerups[:]:
                if now >= pw["end_time"]:
                    self.remove_powerup_effect(pw["type"])
                    self.active_powerups.remove(pw)

        # BALL UPDATE
        for ball in self.balls[:]:
            ball.update()
            if ball.y > SETTINGS["screen_height"]:
                self.balls.remove(ball)

        # cek collision dengan block/paddle
        self.check_collision()

    # ==========================================================
    def apply_powerup(self, ptype):
        if ptype == "extra":
            self.balls.append(Ball(self.paddle.x + self.paddle.width//2, self.paddle.y - 25))
        elif ptype == "expand":
            self.paddle.enlarge()
        elif ptype == "shrink":
            self.paddle.shrink()

    # ==========================================================
    def check_collision(self):
        for ball in self.balls:
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

                        block.destroyed = True
                        ball.dy *= -1

                        # 30% drop
                        if random.random() < 0.3:
                            ptype = random.choice(["extra", "expand", "shrink"])
                            self.powerups.append(PowerUp(block.x + block.width//2, block.y, ptype))

    # ==========================================================
    def draw(self):
        self.paddle.draw(self.screen)

        for ball in self.balls:
            ball.draw(self.screen)

        for b in self.blocks:
            b.draw(self.screen)

        for p in self.powerups:
            p.draw(self.screen)

    # ==========================================================
    def check_win(self):
        return all(b.destroyed for b in self.blocks)

    # ==========================================================
    def run(self):
        pygame.mouse.set_visible(False)
        running = True

        # ======= COUNTDOWN 5 DETIK =======
        start_time = time.time()
        while time.time() - start_time < 5:
            self.screen.fill(BLACK)
            countdown = 5 - int(time.time() - start_time)

            font = pygame.font.Font(None, 80)
            text = font.render(str(countdown), True, RETRO_YELLOW)
            rect = text.get_rect(center=(SETTINGS["screen_width"]//2, SETTINGS["screen_height"]//2))
            self.screen.blit(text, rect)

            pygame.display.flip()
            self.clock.tick(60)

        # ======= MAIN LOOP =======
        while running:
            self.screen.fill(BLACK)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

            # KALAH
            if len(self.balls) == 0:
                running = False
                self.game_over_popup()
                return

            # MENANG
            if self.check_win():
                running = False
                self.win_popup()
                return

    # ==========================================================
    def win_popup(self):
        pygame.mouse.set_visible(True)

        font = pygame.font.Font(None, 60)
        text = font.render("YOU WIN!", True, RETRO_GREEN)
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
                if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

        self.reset()

    # ==========================================================
    def game_over_popup(self):
        pygame.mouse.set_visible(True)

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
                if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

        self.reset()

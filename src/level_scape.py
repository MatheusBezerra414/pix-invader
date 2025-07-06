import pygame
import os
from src.config import BASE_PATH
from src.player import Player

class Obstacle:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "car.png"))
        self.image = pygame.transform.scale(self.image, (180, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, scroll_x):
        screen.blit(self.image, self.rect.move(-scroll_x, 0))

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

class Federal:
    def __init__(self, start_x=-100):
        self.images = [
            pygame.transform.scale(pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "pf_run1.png")), (50, 60)),
            pygame.transform.scale(pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "pf_run2.png")), (50, 60))
        ]
        self.frame = 0
        self.timer = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(start_x, 440))

    def update(self):
        self.rect.x += 1.5
        self.timer += 1
        if self.timer >= 10:
            self.timer = 0
            self.frame = (self.frame + 1) % 2
            self.image = self.images[self.frame]

    def draw(self, screen, scroll_x):
        screen.blit(self.image, self.rect.move(-scroll_x, 0))

    def check_catch(self, player_rect):
        return self.rect.colliderect(player_rect)

class LevelEscape:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.background = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "bg_escape.png"))
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.reset()

    def reset(self):
        self.player = Player(100, 400)
        self.platform = pygame.Rect(0, 500, 2000, 40)
        self.federal = Federal(start_x=-100)
        self.scroll_x = 0

        self.obstacles = [
            Obstacle(600, 400),
            Obstacle(1200, 400),
            Obstacle(1800, 400),
            Obstacle(2400, 400)
        ]

        self.won = False
        self.lost = False
        self.completed = False
        self.awaiting_restart = False
        self.loss_reason = ""

    def update(self, keys):
        if self.awaiting_restart:
            if keys[pygame.K_s]:
                self.reset()
            elif keys[pygame.K_n]:
                self.completed = True
            return

        if self.won or self.lost:
            self.awaiting_restart = True
            return

        self.scroll_x += 6
        self.player.rect.x += 6

        if keys[pygame.K_LEFT]:
            self.player.rect.x -= 6
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += 6

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.player.on_ground:
                self.player.vel_y = self.player.jump_speed

        self.player.vel_y += self.player.gravity
        self.player.rect.y += self.player.vel_y
        self.player.on_ground = False

        if self.player.rect.colliderect(self.platform):
            self.player.rect.bottom = self.platform.top
            self.player.vel_y = 0
            self.player.on_ground = True

        for obs in self.obstacles:
            if obs.check_collision(self.player.rect):
                self.lost = True
                self.loss_reason = "A POLÍCIA FEDERAL TE PEGOU!"

        self.federal.update()
        if self.federal.check_catch(self.player.rect):
            self.lost = True
            self.loss_reason = "A POLÍCIA FEDERAL TE PEGOU!"

        if self.player.rect.x >= 1920:
            self.won = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for obs in self.obstacles:
            obs.draw(self.screen, self.scroll_x)

        self.federal.draw(self.screen, self.scroll_x)

        offset_player = self.player.rect.move(-self.scroll_x, 0)
        self.screen.blit(self.player.image, offset_player)

        if self.won:
            text = self.font.render("VOCÊ FUGIU COM BILHÕES EM PIX!", True, (0, 255, 255))
            self.screen.blit(text, (260, 60))
        elif self.lost:
            text = self.font.render(self.loss_reason, True, (255, 0, 0))
            self.screen.blit(text, (200, 60))

        if self.awaiting_restart:
            retry = self.font.render("Deseja tentar novamente? (S = Sim, N = Não)", True, (255, 255, 255))
            self.screen.blit(retry, (200, 120))
        else:
            info = self.font.render("Corra! Use SETAS e ESPAÇO para fugir da PF", True, (255, 255, 255))
            self.screen.blit(info, (20, 20))

        pygame.display.flip()
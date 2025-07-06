import pygame
import os
from src.config import BASE_PATH
from src.player import Player
from src.item import Token
from src.door import Door
from src.enemy import Enemy

class Firewall:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "firewall.png"))
        self.image = pygame.transform.scale(self.image, (80, 70))
        self.rect = self.image.get_rect(topleft=(x, 500-70))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

class CustomEnemy(Enemy):
    def __init__(self, x, y, patrol_range=100, speed=2):
        super().__init__(x, y, patrol_range, speed)
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "virus.png"))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, 500 - 100))  # Alinha no chão

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class LevelSecurity:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.background = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "bg_security.png"))
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.reset()

    def reset(self):
        self.player = Player(100, 400)
        self.platforms = [
            pygame.Rect(0, 500, 960, 40), 
            pygame.Rect(280, 400, 20, 20),
            pygame.Rect(420, 320, 120, 20),
            pygame.Rect(600, 240, 120, 20)
        ]

        self.token = Token(650, 200)
        self.door = Door(830, 380)

        enemy_x = self.player.rect.right + 150
        self.enemy = CustomEnemy(enemy_x, 460, patrol_range=300)

        self.firewalls = [Firewall(350, 470), Firewall(580, 470)]

        self.token_collected = False
        self.won = False
        self.lost = False
        self.completed = False
        self.awaiting_restart = False

    def update(self, keys):
        if self.awaiting_restart:
            if keys[pygame.K_s]:
                self.reset()
            elif keys[pygame.K_n]:
                self.completed = True
            return

        if self.won:
            self.completed = True
            return

        self.player.update(keys, self.platforms)

        if not self.token_collected:
            self.token_collected = self.token.update(self.player.rect)

        self.won = self.door.update(self.player.rect, self.token_collected)

        self.enemy.update()
        if self.enemy.check_collision(self.player.rect):
            self.lost = True

        for fw in self.firewalls:
            if fw.check_collision(self.player.rect):
                self.lost = True

        if self.lost:
            self.awaiting_restart = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), platform, border_radius=6)

        self.token.draw(self.screen)
        self.door.draw(self.screen)
        self.enemy.draw(self.screen)

        for fw in self.firewalls:
            fw.draw(self.screen)

        self.player.draw(self.screen)

        if self.token_collected:
            text = self.font.render("Token coletado! Vá para o cofre.", True, (255, 255, 255))
            self.screen.blit(text, (40, 40))

        if self.won:
            text = self.font.render("Sistema invadido!", True, (0, 255, 255))
            self.screen.blit(text, (320, 60))
        elif self.lost:
            text = self.font.render("Você foi bloqueado!", True, (255, 0, 0))
            self.screen.blit(text, (320, 60))

        if self.awaiting_restart:
            retry = self.font.render("Deseja tentar novamente? (S = Sim, N = Não)", True, (255, 255, 255))
            self.screen.blit(retry, (200, 120))

        pygame.display.flip()
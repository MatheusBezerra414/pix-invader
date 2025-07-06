import pygame
import random
import os
from src.config import BASE_PATH
from src.player import Player
from src.item import Token

class NPC:
    def __init__(self, x, y_base, index, has_token=False):
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", f"npc{index + 1}.png"))
        self.image = pygame.transform.scale(self.image, (150, 160))
        self.rect = self.image.get_rect(topleft=(x, y_base - self.image.get_height()))
        self.has_token = has_token
        self.interacted = False

    def interact(self):
        self.interacted = True
        return self.has_token

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class LevelBar:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(100, 400)
        self.platforms = [pygame.Rect(0, 500, 960, 40)]

        self.background = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "bg_bar.png"))
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.npcs = []
        self.token_found = False
        self.completed = False
        self.font = pygame.font.SysFont(None, 28)

        token_index = random.randint(0, 3)
        for i in range(4):
            npc = NPC(150 + i * 180, 480, i, has_token=(i == token_index))
            self.npcs.append(npc)

    def update(self, keys):
        self.player.update(keys, self.platforms)

        if keys[pygame.K_e]:
            for npc in self.npcs:
                if self.player.rect.colliderect(npc.rect):
                    if npc.interact():
                        self.token_found = True
                        self.completed = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # for platform in self.platforms:
        #     pygame.draw.rect(self.screen, (80, 50, 80), platform)

        for npc in self.npcs:
            npc.draw(self.screen)

        self.player.draw(self.screen)

        if self.token_found:
            text = self.font.render("Você encontrou a chave de acesso! Indo para próxima fase...", True, (0, 255, 0))
            self.screen.blit(text, (200, 40))
        else:
            text = self.font.render("Aperte E perto de alguém para interagir", True, (255, 255, 255))
            self.screen.blit(text, (20, 20))

        pygame.display.flip()
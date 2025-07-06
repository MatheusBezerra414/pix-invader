import pygame
import os
from src.config import BASE_PATH

class Token:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "token.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def update(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True  
        return False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)
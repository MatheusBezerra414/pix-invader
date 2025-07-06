import pygame
import os
from src.config import BASE_PATH

class Door:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.image_locked = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "cofre_2.png"))
        self.image_open = pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "cofre.png"))
        self.image_locked = pygame.transform.scale(self.image_locked, (120, 140))
        self.image_open = pygame.transform.scale(self.image_open, (120, 140))
        
        self.is_open = False
        self.react = self.image_locked.get_rect(topleft=(x, y))

    def update(self, player_rect, token_collected):
        if token_collected:
            self.is_open = True

        if self.is_open and self.rect.colliderect(player_rect):
            return True  
        return False

    def draw(self, screen):
        image = self.image_open if self.is_open else self.image_locked
        screen.blit(image, self.rect)
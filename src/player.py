import pygame
import os
from src.config import BASE_PATH

class Player:
    def __init__(self, x, y):
        self.images_idle = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "player_idle1.png")), (140, 150)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "player_idle2.png")), (140, 150)
            )
        ]
        self.image_jump = pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_PATH, "assets", "images", "player_jump.png")), (140, 150)
        )

        self.image = self.images_idle[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_speed = -25
        self.gravity = 1
        self.on_ground = False

        self.animation_timer = 0
        self.frame = 0

    def update(self, keys, platforms):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = self.jump_speed

        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.check_collision(platforms, dx=True)
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision(platforms, dy=True)

        # 👇 animação dinâmica
        if not self.on_ground:
            self.image = self.image_jump
        elif self.vel_x != 0:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % 2
            self.image = self.images_idle[self.frame]
        else:
            self.image = self.images_idle[0]

    def check_collision(self, platforms, dx=False, dy=False):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx:
                    if self.vel_x > 0:
                        self.rect.right = platform.left
                    elif self.vel_x < 0:
                        self.rect.left = platform.right
                if dy:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = platform.bottom
                        self.vel_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
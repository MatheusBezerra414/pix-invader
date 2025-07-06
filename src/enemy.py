import pygame

class Enemy:
    def __init__(self, x, y, patrol_range=100, speed=2):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (255, 50, 50)
        self.start_x = x
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
import pygame
from src.level_bar import LevelBar
from src.level_security import LevelSecurity
from src.level_scape import LevelEscape
from src.player import Player
from src.item import Token
from src.door import Door
from src.enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)

        self.level_index = 0
        self.levels = [
            LevelBar(screen),
            LevelSecurity(screen),
            LevelEscape(screen)
        ]
        self.current_level = self.levels[self.level_index]

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.current_level.update(keys)

        if hasattr(self.current_level, "completed") and self.current_level.completed:
            pygame.time.delay(1000)
            self.next_level()

    def draw(self):
        self.current_level.draw()

    def next_level(self):
        self.level_index += 1
        if self.level_index < len(self.levels):
            self.current_level = self.levels[self.level_index]
        else:
            self.running = False  
import pygame
from pathlib import Path
import sys
sys.path.append('..')

"""
class for the overlay that displays the player's health and score, as well as the
death message
"""
class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        self.rect = self.image.get_rect()
        folder = Path("./")
        file = folder / "virus.ttf"
        self.font = pygame.font.Font('./font/virus.ttf', 32)
        self.text = self.font.render('Health: 100       Score: 0', True, (255, 255, 255))
        
    def render(self, text):
        self.text = self.font.render(text, True, (0, 0, 0))
        self.image.blit(self.text, self.rect)
    
    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    """
    update text with current health and score
    """
    def update(self, score, health):
        self.text = self.font.render('Health: ' + str(health) + '      Score: ' + str(score), True, (255, 255, 255))

    """
    sets up the loooooooooser message
    """
    def youLost(self):
        self.font = pygame.font.Font('./font/virus.ttf', 24)
        self.text = self.font.render('You did not win the game. It was never winnable...', True, (255, 255, 255))

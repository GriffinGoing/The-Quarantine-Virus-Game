import pygame
from classes import projectile

"""
Player class for, well, the player. You gon' git burnt tho
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.moveSpeed = 20
        self.moveTicker = 0
        self.damage = 10
        self.loadSprite('./sprites/spaceship/Ships/Medium/body_01.png')
        self.shootSound = pygame.mixer.Sound('./sounds/151014__bubaproducer__laser-classic-shot-1.ogg')

    """
    loads the player sprite
    @param path the filepath to the player sprite. supports one sprite currently
    """
    def loadSprite(self, path):
        newImage = pygame.image.load(path).convert_alpha()
        newImage = pygame.transform.scale(newImage, (40, 70))
        self.image = newImage
        self.rect = self.image.get_rect()
        self.rect.x = 376
        self.rect.y = 530

    """
    takes health away (takes damage).
    @param damage the amount of health to lose.
    """
    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0: self.health = 0

    """
    is the player dead? maybs...
    """
    def isDead(self):
        if (self.health <= 0):
            return True
        else:
            return False

    """
    don't make me tell you what this does...
    """
    def move_left(self):
        self.rect.x -= self.moveSpeed
        if (self.rect.x < 0): self.rect.x = 795

    """
    see above. 
    """
    def move_right(self):
        self.rect.x += self.moveSpeed
        if (self.rect.x > 790): self.rect.x = 0

    """
    hit 'em with the pew pew 
    """
    def shoot(self):
        self.shootSound.play()
        newProj = projectile.Projectile(True, (self.rect.x + 12.5), self.rect.y + 1, 10)
        return newProj



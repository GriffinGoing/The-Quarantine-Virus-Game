import pygame
import random
from classes import projectile
from classes import game

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.health = 5
        self.moveSpeed = 1
        self.damage = 10
        self.loadSprites(sprites)
        self.rect.x = x
        self.rect.y = y
        self.shootSound = pygame.mixer.Sound('./sounds/151019__bubaproducer__laser-shot-element-1.ogg')

    """
    loads the preset enemy sprites in, as reconverting would be (and was) a major drain on
    power and performance
    @param sprites the sprite(s) to be loaded in
    """
    def loadSprites(self, sprites):
        self.sprites = sprites
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.imageNum = 0

    """
    moves to the next image 1 in 10 times, which creates a random fascade of virus sprites that dazzle the eye
    as they come closer to killing the player.
    """
    def iterateImage(self):
        rando = random.randint(0, 100)
        if (rando >= 90):
            self.imageNum += 1
            if (self.imageNum > (len(self.sprites)-1)): self.imageNum = 0
        self.image = self.sprites[self.imageNum]

    """
    returns if the eemy is dead. an auxilary function if health is ever modified or bosses are introduced
    """
    def isDead(self):
        if (self.health <= 0): return True
        else: return False

    """
    moves the enemy by one iteration of the moveSpeed
    """
    def move(self):
        self.rect.y += self.moveSpeed
        if (self.rect.y < 0): self.rect.y = 0

    """
    makes and returns a projectile object
    """
    def shoot(self):
        self.shootSound.play()
        newProj = projectile.Projectile(False, (self.rect.x + 20), self.rect.y + 25, 3)
        return newProj

    """
    checks for collisions with the player
    @param game the game in which the enemy exists
    """
    def update(self, game):
        # check for player impacts
        hitPlayer = pygame.sprite.spritecollideany(self, game.playerGroup)
        if hitPlayer:
            game.player.takeDamage(20)
            self.kill()
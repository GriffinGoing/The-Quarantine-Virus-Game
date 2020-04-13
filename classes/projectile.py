import pygame
from classes import  game

"""
Projectile class for the big ol' guns (small ones too)
"""
class Projectile(pygame.sprite.Sprite):
    def __init__(self, fromPlayer, x, y, moveSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.damage = 10
        self.moveSpeed = moveSpeed
        self.fromPlayer = fromPlayer
        if (fromPlayer): self.loadPlayerProj()
        else: self.loadEnemyProj()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """
    loads in the player projectile images, as player and enemy projectiles are different
    """
    def loadPlayerProj(self):
        self.sprites = []
        for i in range(1, 4):
            path = './sprites/projectiles/player-new-projectile1-' + str(i) + '.png'
            newImage = pygame.image.load(path).convert_alpha()
            newImage = pygame.transform.scale(newImage, (15, 25))
            self.sprites.append(newImage)
        self.image = self.sprites[0]
        self.imageNum = 0

    """
    loads enemy projectile images
    """
    def loadEnemyProj(self):
        self.sprites = []
        for i in range(1, 4):
            path = './sprites/projectiles/new-projectile1-' + str(i) + '.png'
            newImage = pygame.image.load(path).convert_alpha()
            newImage = pygame.transform.scale(newImage, (10, 18))
            self.sprites.append(newImage)
        self.image = self.sprites[0]
        self.imageNum = 0

    """
    modifies projectile speeds, damages, and origins
    @param speed the speed the projectile will move
    @param damage the damage the projectile will do
    @param fromPlayer if true, the projectile originated from the player. else, from an enemy. 
    """
    def setupProjectile(self, speed, damage, fromPlayer):
        self.damage = damage
        self.speed = speed
        self.fromPlayer = fromPlayer

    """
    moves up for enemies, down for players
    """
    def move(self):
        if (self.fromPlayer): self.rect.y -= self.moveSpeed
        else: self.rect.y += self.moveSpeed

    """
    animates the projectile
    """
    def iterateImage(self):
        self.imageNum += 1
        if (self.imageNum > (len(self.sprites) - 1)): self.imageNum = 0
        self.image = self.sprites[self.imageNum]

    """
    checks for collisions with either the player or the enemies
    """
    def update(self, game):
        if self.fromPlayer:
            #check for enemy impacts
            hitEnemy = pygame.sprite.spritecollideany(self, game.enemies)
            if hitEnemy:
                hitEnemy.kill()
                game.incScore()
                self.kill()
        else:
            #check for player impacts
            hitPlayer = pygame.sprite.spritecollideany(self, game.playerGroup)
            if hitPlayer:
                game.player.takeDamage(10)
                self.kill()
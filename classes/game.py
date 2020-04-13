import pygame
import random
import time
"""
wildcard import didn't work w/ classes w/ or w/out sys.append, idk why but this is late 
so i just gave in and kindly deflowered myself *angry face* 
"""
from classes import player
from classes import overlay
from classes import enemy
from classes import projectile

"""
The Game class, which stores and handles/runs the game
"""
class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('./sounds/burning-mir__organic-metalic-ambience.ogg')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        #self.healthPickupEvent = pygame.event.Event(pygame.USEREVENT + 1)
        self.enemies = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.overlay = overlay.Overlay()
        self.screen.fill((255, 255, 255))
        self.ready = True 
        self.score = 0
        self.player = player.Player()
        self.playerGroup.add(self.player)
        self.background = self.loadBackground()
        self.enemyImages = self.loadEnemyImages()
        self.enemyCounter = 1
        self.makeEnemyDelay = 1001

    """
    Creates enemies. Uses exponential growth to model the growth of virus transmission. Automatically relocates sprites
    to a new row, allowing 16 at most to a row. Calculates x offsets and grows y spacing appropriately. 
    just thought it would be cool if new enemies grew from each other but hey, next time right?
    """
    def proliferateEnemies(self):
        ySpacing = 0
        enemyInRowCounter = 0
        if (self.makeEnemyDelay > 800):
            if (self.enemyCounter == 1):
                offset = 400
                spacing = 0
            elif (self.enemyCounter > 16):
                offset = (800 / 16) / 16
                spacing = 800 / 16
            else:
                offset = (800 / self.enemyCounter) / self.enemyCounter
                spacing = 800 / self.enemyCounter
            #rowCounter = 0
            for i in range(0, self.enemyCounter):
                newEnemy = enemy.Enemy((offset + (enemyInRowCounter * spacing)), (25 + ySpacing), self.enemyImages)
                self.enemies.add(newEnemy)
                enemyInRowCounter += 1
                if (enemyInRowCounter > 15):
                    enemyInRowCounter = 0
                    ySpacing += 20

            if self.enemyCounter > 1: self.enemyCounter = self.enemyCounter * self.enemyCounter
            else: self.enemyCounter += 1
            self.makeEnemyDelay = 0

        else: self.makeEnemyDelay += 1

    """
    loads in the background image for the game
    """
    def loadBackground(self):
        newImage = pygame.image.load('./sprites/spaceship/Background/stars_texture.png').convert_alpha()
        newImage = pygame.transform.scale(newImage, (800, 600))
        newImage.set_alpha(255)
        return newImage

    """
    loads and stores an array of enemy sprites for enemy animation. saves on processing power, which is important
    due to the exponential proliferation of enemies
    """
    def loadEnemyImages(self):
        enemyImages = []
        for i in range(21):
            path = './sprites/virus/Virus' + str(i) + '.png'
            #print(i)
            print(path)
            newImage = pygame.image.load(path).convert_alpha()
            newImage = pygame.transform.scale(newImage, (50, 50))
            enemyImages.append(newImage)
        return enemyImages

    """
    increments score
    """
    def incScore(self):
        self.score += 1

    """
    runs the game while the game is not over. 
    """
    def run(self):
        self.done = False
        while not self.done:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0)) #add background
            self.proliferateEnemies() #make enemies

            #for enemies to animate, move, shoot
            for enemy in self.enemies.sprites():
                enemy.move()
                enemy.iterateImage()
                rando = random.randint(0, 1000)
                if (rando > 995):
                    self.projectiles.add(enemy.shoot())
                if (enemy.rect.y == 600):
                    self.player.takeDamage(10)
                    enemy.kill()
                enemy.update(self)

            #animate projectiles and check for impacts
            for projectile in self.projectiles.sprites():
                projectile.move()
                projectile.iterateImage()
                projectile.update(self)
                if (projectile.rect.y < 0 or projectile.rect.y > 600):
                    projectile.kill()

            #still alive???
            if (self.player.isDead()): self.done = True

            #check for key events and act accordingly
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    if event.key == pygame.K_SPACE:
                        self.projectiles.add(self.player.shoot())
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()

            #update and fill in screen
            self.overlay.update(self.score, self.player.health)
            self.projectiles.draw(self.screen)
            self.enemies.draw(self.screen)
            self.overlay.draw(self.screen)
            self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
            pygame.display.flip()
            self.clock.tick(60)

            #when the player dies
            if self.player.isDead():
                self.done = True
                time.sleep(1)
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.background, (0, 0))
                self.overlay.youLost()
                self.projectiles.draw(self.screen)
                self.enemies.draw(self.screen)
                self.overlay.draw(self.screen)
                self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                pygame.display.flip()
                time.sleep(3)





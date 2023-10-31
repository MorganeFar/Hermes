import pygame, sys
sys.path.append(".\\code\\global_niveau")
from settings import *
from level import Level
from game_data import level_1


#setup 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen) #pour avoir run autre level il suffit juste de changer 'level_1' par un autre nom de level

background = pygame.image.load(".\\design\\niveau1\\background.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()

def start():
    level.__init__(level_1, screen) # s'assure de reinitialiser le niveau (eviter qu'on soit mort avant d'avoir recommence)
    while not level.isDead : 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(fond, (0,0))
        level.run()      
    
        pygame.display.update()
        clock.tick(60)
# -*- coding: utf-8 -*-
"""
clear code le platformer complet, partie 2 sur le visual level editor 
"""
import pygame, sys
sys.path.append("../global_niveau")
from settings import *
from level import Level
from game_data import level_1


#setup 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen) #pour avoi run autre level il suffit juste de changer 'level_1' par un autre nom de level

background = pygame.image.load("../../design/niveau1/background.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()

while True : 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #screen.fill('grey')
    screen.blit(fond, (0,0))
    
    level.run()
    
    pygame.display.update()
    clock.tick(60)
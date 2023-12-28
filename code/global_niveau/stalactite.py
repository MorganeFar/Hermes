# -*- coding: utf-8 -*-
"""
stalactite
"""

import pygame
from tiles import AnimatedTile

class Stalactite(AnimatedTile):
    def __init__(self,size,x,y,path,actif,value): #actif est un booleen qui dit si le stalactite bouge ou pas, a voir si on le garde la dedans ou dans le niveau  
        super().__init__(size,x,y,path)
        self.rect.y += size - self.image.get_size()[1] #reposotionne les stalactite 
        self.speed = 8
        self.actif = actif
        self.value = value
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.8

    def fall(self):
        #self.rect.y += self.speed 
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y
        
    def active(self, actif):
        self.actif = actif

    def update(self,shift):
        self.rect.x += shift 
        if self.actif :
            self.fall()
        
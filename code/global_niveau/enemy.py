# -*- coding: utf-8 -*-
"""
clear code le platformer complet, partie 2 sur le visual level editor, enemy 
"""

import pygame
from tiles import AnimatedTile 
from random import randint 

"""
class Enemy(AnimatedTile):
    def __init__(self,size,x,y,path,offset):
        super().__init__(size,x,y,path)
        offset_y = y - offset 
        self.rect.topleft = (x,offset_y)
"""

class Enemy(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)
        self.rect.y += size - self.image.get_size()[1] #reposotionne les enemies 
        self.speed = randint(2,3)

    def move(self):
        self.rect.x += self.speed 
        
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def reverse(self): #si on appelle la fct le monstre va dans l'autre sens 
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift 
        self.animate()
        self.move()
        self.reverse_image()
        
        
        
        
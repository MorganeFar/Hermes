# -*- coding: utf-8 -*-
"""
tiles
"""

import pygame
from support import import_folder
# DEBUG
from settings import screen_height, screen_width
screen = pygame.display.set_mode((screen_width, screen_height))

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift 
        
class StaticTile(Tile):
    def __init__(self, size, x, y, surface, value):
        super().__init__(size, x, y)
        self.image = surface 
        self.value = value
        
class AnimatedTile(Tile): #pour avoir du decor anime 
     def __init__(self, size, x, y, path):
         super().__init__(size,x,y)
         self.frames = import_folder(path)
         self.frame_index = 0 
         self.image = self.frames[self.frame_index]
         
     def animate(self):
         self.frame_index += 0.15 #gere le vitesse d'animation 
         if self.frame_index >= len(self.frames):
             self.frame_index = 0
         self.image = self.frames[int(self.frame_index)]
         
     def update(self, shift):
         self.animate()
         self.rect.x += shift

         
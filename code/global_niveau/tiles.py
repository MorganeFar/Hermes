# -*- coding: utf-8 -*-
"""
tiles
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from support import import_folder
# ----------------------------------------------

# Class pour les tiles classiques
class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift 

# Class pour les tiles statiques 
class StaticTile(Tile):
    def __init__(self, size, x, y, surface, value):
        super().__init__(size, x, y)
        self.image = surface 
        self.value = value

# Class pour les tiles abnimes (monstre par exemple)
class AnimatedTile(Tile): 
     def __init__(self, size, x, y, path):
         super().__init__(size,x,y)
         self.frames = import_folder(path)
         self.frame_index = 0 
         self.image = self.frames[self.frame_index]
         
     def animate(self):
         self.frame_index += 0.15 # Gere la vitesse d'animation 
         if self.frame_index >= len(self.frames):
             self.frame_index = 0
         self.image = self.frames[int(self.frame_index)]
         
     def update(self, shift):
         self.animate()
         self.rect.x += shift

# Class pour le terrain du niveau 5 qui bouge constament 
class TileLevel5(Tile):
    def __init__(self, size, x, y, surface, value):
        super().__init__(size, x, y)
        self.image = surface 
        self.value = value
        
    def update(self, shift): # Le shift est la vitesse a laquelle le monde bouge 
        self.rect.y -= shift

# -*- coding: utf-8 -*-
"""
enemy 
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from tiles import AnimatedTile 
from random import randint
# ----------------------------------------------

class Enemy(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)
        if path == '../../design/niveau2/monster/poulpe': # Cas particulier du poulpe
            self.rect = self.image.get_rect(midtop=(x, y)) 
            self.rect[3] = self.rect[3]-15  # Reduit taille du rect de collision avec le pouple
            self.rect.y += size - self.image.get_size()[1]  # Reposotionne les enemies
        else:
            self.rect = self.image.get_rect(midtop=(x, y))
            self.rect.y += size - self.image.get_size()[1]  # Reposotionne les enemies
        self.speed = randint(2, 3) # La vitesse des ennemies est aleatoire entre 2 et 3

    # Fait en sorte que l'enneie bouge 
    def move(self):
        self.rect.x += self.speed 

    # Fait en sorte que l'image de l'ennemie se retourne quand il a une vitesse negative 
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    # Fait en sorte que le monstre aille dans l'autre sens (il lui met une vitesse negative)
    def reverse(self): 
        self.speed *= -1

    # Ce qui est constament recalculer pour update les ennemies 
    def update(self,shift):
        self.rect.x += shift 
        self.animate()
        self.move()
        self.reverse_image()
        

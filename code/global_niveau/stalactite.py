# -*- coding: utf-8 -*-
"""
stalactite
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from tiles import AnimatedTile
# ----------------------------------------------

class Stalactite(AnimatedTile):
    def __init__(self,size,x,y,path,actif,value): # Actif est un booleen qui dit si le stalactite bouge ou pas 
        super().__init__(size,x,y,path)
        self.rect.y += size - self.image.get_size()[1] # Reposotionne les stalactite 
        self.speed = 8 # La vitesse
        self.actif = actif # Si il es active ou non 
        self.value = value # Sa valeur, cela va nous indiquer lequl est active 
        self.direction = pygame.math.Vector2(0,0) # On utilise un vecteur pour la direction 
        self.gravity = 0.8 # On applique la gravite aux stalactite 

    # Quand il tombe 
    def fall(self):
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y

    # Il est active 
    def active(self, actif):
        self.actif = actif

    # Ce qui est recalcule pendant le jeu 
    def update(self,shift):
        self.rect.x += shift 
        if self.actif :
            self.fall()
        

# -*- coding: utf-8 -*-
"""
stalactite
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from tiles import AnimatedTile
# ----------------------------------------------


class Stalactite(AnimatedTile):
    def __init__(self, size, x, y, path, actif, value):
        # Actif est un booleen qui indique si le stalactite bouge ou pas
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]  # Repositionne les stalactites
        self.actif = actif  # S'il est actif ou non
        self.value = value  # Indiquer quel stalactite est actif
        self.direction = pygame.math.Vector2(0, 0)  # Utilisation d'un vecteur pour la direction
        self.gravity = 0.8  # On applique la gravite aux stalactites

    # Quand il tombe 
    def fall(self):
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y

    # Il est actif
    def active(self, actif):
        self.actif = actif

    # Ce qui est recalcule pendant le jeu 
    def update(self, shift):
        self.rect.x += shift 
        if self.actif:
            self.fall()
        

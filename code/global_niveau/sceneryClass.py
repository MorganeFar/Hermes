"""
scenery 
"""

# ---------------- IMPORTATIONS ----------------
import pygame, sys
from settings import screen_height, screen_width
screen = pygame.display.set_mode((screen_width, screen_height))
# ----------------------------------------------

# Class pour mettre en place des scenes 
class Scenery(pygame.sprite.Sprite):
    def __init__(self, pos_x_coef, pos_y_coef, widthCoef, heightCoef, pics):
        super().__init__()
        self.sprites = [] # Les sprites sont au depart un tableau vide 
        self.current_sprite = 0 # L'imae actuelle 
        self.begin = True # Correspond à toLeft pour charon et zoomIn pour retry
        self.move = 0
        self.moveX = 1
        for pic in pics:
            self.sprites.append((pygame.transform.scale(pygame.image.load(pic), (screen_width*widthCoef, screen_height*heightCoef))))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        pygame.draw.rect(screen, (0, 0, 255), self.image.get_rect(), 2)
        self.rect.topleft = [pos_x_coef*screen_width, pos_y_coef*screen_height]
        
    def update(self, speed, move):
        self.move = move
        if self.moveX >= move:
            self.begin = not self.begin
            self.moveX = 0
        self.moveX += speed 

    # Fait en sorte que Charon bouge 
    def move_left(self):
        if self.begin:
            self.rect.x -= int(self.move)
        else:
            self.rect.x += int(self.move)  

    # Fait en sorte que le bouton retry zoom et dezoom 
    def zoom(self):
        # Fait un changement d'image entre l'une petite et l'autre plus grande
        self.image = self.sprites[int(self.moveX)]

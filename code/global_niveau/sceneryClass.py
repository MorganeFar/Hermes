
import pygame, sys
from settings import screen_height, screen_width

class Scenery(pygame.sprite.Sprite):
    def __init__(self, pos_x_coef, pos_y_coef, widthCoef, heightCoef, pics):
        super().__init__()
        self.sprites = []
        self.current_sprite = 0
        self.begin = True #correspond à toLeft pour charon et zoomIn pour retry
        self.move = 0
        self.moveX = 1
        for pic in pics:
            self.sprites.append((pygame.transform.scale(pygame.image.load(pic), (screen_width*widthCoef, screen_height*heightCoef))))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x_coef*screen_width, pos_y_coef*screen_height]
        
        
    def update(self, speed, move):
        self.move = move
        if self.moveX >= move:
            self.begin = not self.begin
            self.moveX = 0
        self.moveX += speed 
        
    def move_left(self):
        if self.begin:
            self.rect.x -= int(self.move)
        else:
            self.rect.x += int(self.move)  
    
    def zoom(self):
        # fait un changement d'image entre l'une petite et l'autre plus grande
        self.image = self.sprites[int(self.moveX)]
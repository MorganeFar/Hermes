# -*- coding: utf-8 -*-
"""
UI (user interface)
"""

import pygame

class UI: 
    def __init__(self, surface, current_level):
        #setup
        self.display_surface = surface 
        
        #level
        self.current_level = current_level
        
        #couleur du texte des objets :
        self.couleur = 'black'
        if self.current_level == 4:
            self.couleur = 'white'
        
        #item (pas forcement besoin, a voi ce qu'il va faire avec)
        self.item = pygame.image.load('../../design/ui/backpack.png').convert_alpha()
        self.item_rect = self.item.get_rect(topleft = (20,61))
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        
    def show_health(self,current):
        if current == 3:
            self.health_bar = pygame.image.load('../../design/ui/heart/6.png').convert_alpha()
        elif current == 2:
            self.health_bar = pygame.image.load('../../design/ui/heart/4.png').convert_alpha()
        elif current == 1:
            self.health_bar = pygame.image.load('../../design/ui/heart/2.png').convert_alpha()
        else:
            self.health_bar = pygame.image.load('../../design/ui/heart/0.png').convert_alpha()
        self.display_surface.blit(self.health_bar,(20,20))
    
    def show_item(self,lequel):
        self.display_surface.blit(self.item, self.item_rect)
        item_text_surf = self.font.render(lequel,False,self.couleur)
        item_text_rect = item_text_surf.get_rect(midleft = (self.item_rect.right+15 ,self.item_rect.centery))
        self.display_surface.blit(item_text_surf, item_text_rect)

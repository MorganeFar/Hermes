# -*- coding: utf-8 -*-
"""
player
"""

import pygame 
from support import import_folder 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 
        self.animation_speed = 0.15 #a changer si on veut une animation plus lente /plus rapide (0.15/0.3/0.45/0.6/0.75/0.9/1.05) 
        self.image = self.animations['stand'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        #player mouvement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8 
        self.gravity = 0.8
        self.jump_speed = -16 #a changer si on veut des sauts moins hauts 
        
        #player status 
        self.status = 'stand'
        self.facing_right = True #va vers la droite 
            #on met les retangles proprement 
        self.on_ground = False 
        self.on_ceiling = False 
        self.on_left = False 
        self.on_right = False 
        
    def import_character_assets(self):
        #'../../design/hermes/'
        character_path = '.\\design\\hermes\\'
        self.animations = {'stand':[], 'run':[], 'jump':[], 'fly':[], 'swim':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = import_folder(full_path)
        
    def animate(self): #on choisi l action du perso (run, fly, jump, stand et autre), donc on recup son etat 
        animation = self.animations[self.status]
        
        #loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): #si on depase le tableau on revient au debut 
            self.frame_index = 0 
        
        image = animation[int(self.frame_index)]
        if self.facing_right: #si on va vers la droite on tourne pas les images 
            self.image = image
        else: #permet de retrourner les images 
            flipped_image = pygame.transform.flip(image, True, False) #flippe horizontaly(x) and verticaly(y) 
            self.image = flipped_image
        
        """
        #set the rectangle, on prend toutes les situations possibles, enleve certains bugs 
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        #else:
            #self.rect = self.image.get_rect(center = self.rect.center)
       """
        
    def get_input(self): #on fait bouger le personnage suivant les touches 
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True 
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False 
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and self.on_ground: #il peut sauter que si il est sur le sol 
            self.jump()
            
    def get_status(self): #on recup l etat du player (jump, stand, run, ...)
        if self.direction.y < 0: #si il va vers le haut 
            self.status = 'jump'
        elif self.direction.y > 1: #si il va vers le bas 
            self.status = 'stand' #ou fall si on avait des sprites de fall 
        else:
            if self.direction.x != 0: #si il va dans une direction c est qu il cours 
                self.status = 'run'
            else:
                self.status = 'stand'
    
    def apply_gravity(self): #sert pour le saut 
        self.direction.y += self.gravity   
        self.rect.y += self.direction.y 
        
    def jump(self):
        self.direction.y = self.jump_speed 
    
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        
        
        

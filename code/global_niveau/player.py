# -*- coding: utf-8 -*-
"""
player
"""

import pygame 
from support import import_folder 
from math import sin 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_health):
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
        
        #health management 
        self.change_health = change_health
        self.invincible = False 
        self.invincibility_duration = 500
        self.hurt_time = 0
        
        #audio 
        self.jump_sound = pygame.mixer.Sound('../../audio/jump.wav')
        self.jump_sound.set_volume(0.1)
        
    def import_character_assets(self):
        character_path = '../../design/hermes/'
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
        
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
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
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground: #il peut sauter que si il est sur le sol 
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
        self.jump_sound.play()
    
    def get_damage(self):
        if not self.invincible:
            self.change_health(-1)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0
    
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()
        
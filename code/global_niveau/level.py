# -*- coding: utf-8 -*-
"""
level
"""

import pygame
from support import import_csv_layout, import_cut_graphic, import_folder
from settings import tile_size, screen_height, screen_width 
from tiles import Tile, StaticTile, AnimatedTile
from enemy import Enemy 
from player import Player 

class Level :
    def __init__(self, level_data,surface):
        #general setup
        self.display_surface = surface 
        self.world_shift = 0
        self.current_x = None
        self.current_y = None 
        self.isDead = False
        
        #player 
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain') #ici le terrain est le nom de l'image de tuile, a voir si on peut mettre plusieurs tuiles pour 1 map

        #item setup
        item_layout = import_csv_layout(level_data['item'])
        self.item_sprites = self.create_tile_group(item_layout, 'item')
        
        #enemy 
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        
        #constraints 
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout): #on met un numero a nos row pour mieux les distinguer et les reperer plus facilement 
            for col_index,val in enumerate(row): #pour chaque indice et chaque valeur de case 
                if val != '-1': #si il y a qqch dans la case 
                    x = col_index * tile_size  
                    y = row_index * tile_size 
                    
                    if type == 'terrain':
                        #terrain_tile_list = import_cut_graphic('../../niveaux/nv_1_apollon/tiles/midTile_1.png')
                        terrain_tile_list = import_folder('../../design/niveau1/tiles')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'item':
                        #sprite = AnimatedTile(tile_size, x, y, '../../niveaux/nv_1_apollon/object')
                        item_tile_list = import_folder('../../design/niveau1/object')
                        tile_surface = item_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'enemies': #a voir apres avec val si on peut avir les autres monstres (attention changer les dossiers)
                        if val == '0':
                            sprite = Enemy(tile_size,x,y,'../../design/niveau1/monster/cyclope_w')
                        if val == '1':
                            sprite = Enemy(tile_size,x,y,'../../design/niveau1/monster/satyr')
                        if val == '2':
                            sprite = Enemy(tile_size,x,y,'../../design/niveau1/monster/cow_1')
                        if val == '3':
                            sprite = Enemy(tile_size,x,y,'../../design/niveau1/monster/cow_2')
                        
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
        
    def player_setup(self,layout):
        for row_index, row in enumerate(layout): 
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1': #le player
                    sprite = Player((x,y))
                    self.player.add(sprite)
                if val == '0': #le goal 
                    fin_surface = pygame.image.load('../../design/global/flag.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,fin_surface)
                    self.goal.add(sprite)
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
        
    def horizontal_mouvement_collision(self):
        player = self.player.sprite 
        player.rect.x += player.direction.x * player.speed #on applique le mouvement horizontal
        
        for sprite in self.terrain_sprites.sprites(): #si le pesro touche un mur en x (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: #si le perso touche un truc alors qu'il va a gauche 
                    player.rect.left = sprite.rect.right
                    player.on_left = True 
                    self.current_x = player.rect.left 
                elif player.direction.x > 0: #si le perso touche qqch alors qu'il va a droite 
                    player.rect.right = sprite.rect.left 
                    player.on_right = True 
                    self.current_x = player.rect.right
                
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0): #on ne touche plus qqch à gauche si on va à droite ou si on passe au dessus de ce mur 
            player.on_left = False 
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False 

    def dead(self):
        # hermes meurt s'il tombe trop bas
        self.current_y = self.player.sprite.rect.top
        self.isDead =  self.current_y > screen_height + 50
        return self.isDead

    def vertical_mouvement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.terrain_sprites.sprites(): #si le pesro touche un mur en y (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: #si le perso touche un truc alors qu'il va vers le bas  
                    player.rect.bottom = sprite.rect.top 
                    player.direction.y = 0 #cela evite que la gravité augmente trop et fait passer le pero a travers les plateformes
                    player.on_ground = True #il est bien sur le sol 
                elif player.direction.y < 0: #si le perso touche qqch alors qu'il va vers le haut 
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True 
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: #si il touche le sol puis tombe ou saute 
            player.on_ground = False 
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False 
        
    def scroll_x(self): #on fait en sorte que le niveau scroll si le perso avance 
        player = self.player.sprite 
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        #la vitesse du pero est nulle et c'est le scroll qui remplace le mouvement du perso 
        if player_x < screen_width/3 and direction_x < 0: #direction a gauche 
            self.world_shift = 8 
            player.speed = 0 
        elif player_x > screen_width - (screen_width/3) and direction_x > 0: #direction a droite 
            self.world_shift = -8
            player.speed = 0 
        else:
            self.world_shift = 0 
            player.speed = 8  
        
    def run(self):

        #run the entier game/level
        
        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift) #on ne dessine pas les constraints car on ne veux pas les voir mais on veut qu'elles existent 
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        #item 
        self.item_sprites.update(self.world_shift)
        self.item_sprites.draw(self.display_surface)
    
        #player sprite
        self.player.update()
        self.horizontal_mouvement_collision()
        self.vertical_mouvement_collision()
        self.scroll_x()
        self.dead()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
    

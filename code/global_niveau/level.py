# -*- coding: utf-8 -*-
"""
level
"""

import pygame
import time
from support import import_csv_layout, import_cut_graphic, import_folder
from settings import tile_size, screen_height, screen_width 
from tiles import Tile, StaticTile, AnimatedTile
from enemy import Enemy 
from player import Player 
from game_data import levels

pygame.init()

### LEVEL 2 ###
screen = pygame.display.set_mode((screen_width, screen_height))
timeFont = pygame.font.Font(None, 50)
TIME_TO_BREATH = 20

class Level :
    def __init__(self, current_level, surface, create_overworld, change_item, change_health):
        # general setup
        self.display_surface = surface 
        self.world_shift = 0
        self.current_x = None
        
        # audio
        self.item_sound = pygame.mixer.Sound('../../audio/item.ogg')
        self.hit_sound = pygame.mixer.Sound('../../audio/hit.wav')
        self.win_sound = pygame.mixer.Sound('../../audio/victory.wav')
        
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.level_data = levels[self.current_level]  # permet de le mettre en paramètre du player

        self.new_max_level = self.level_data['unlock']
        self.the_fond = pygame.image.load('../../design/niveau' + str(
            self.current_level) + '/background.png').convert_alpha()
        self.tab_level = self.level_data['items']

        if self.current_level == 2:
            self.current_time = 0
            self.timeSinceLastBreath = round(time.time())  # get the number of seconds since epoch
            # cf. epoch = moment where time begins => 1 january 1970 00:00:00
            self.timeTab = []
            for i in range(20):
                self.timeTab.append(str(i+1))
            self.timer()

        # monsters
        self.tab_monsters = self.level_data['monsters']

        # player
        player_layout = import_csv_layout(self.level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        self.isDead = False
        self.isBreathing = True

        # user interface
        self.change_item = change_item
        
        # terrain setup
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')  # ici le terrain est le nom de l'image de tuile, a voir si on peut mettre plusieurs tuiles pour 1 map

        # item setup (aussi a changer dans game_data, map test du niveau 1) item0 item1 item2 et du coup item0_sprite item1_sprite item2_sprite, en essayant de les laisser dans les fichiers design tels qu'ils sont
        item_layout = import_csv_layout(self.level_data['item'])
        self.item_sprites = self.create_tile_group(item_layout, 'item')
        
        # enemy
        enemy_layout = import_csv_layout(self.level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        
        # constraints
        constraint_layout = import_csv_layout(self.level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):  # on met un numero a nos row pour mieux les distinguer et les reperer plus facilement
            for col_index, val in enumerate(row):  # pour chaque indice et chaque valeur de case
                if val != '-1': # si il y a qqch dans la case
                    x = col_index * tile_size  
                    y = row_index * tile_size 
                    
                    if type == 'terrain':
                        # terrain_tile_list = import_cut_graphic('../../niveaux/nv_1_apollon/tiles/midTile_1.png')
                        path = '../../design/niveau' + str(self.current_level) + '/tiles'
                        terrain_tile_list = import_folder(path)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        
                    if type == 'item':  # item0 item1 item2
                        # sprite = AnimatedTile(tile_size, x, y, '../../niveaux/nv_1_apollon/object')
                        path = '../../design/niveau' + str(self.current_level) + '/object'
                        item_tile_list = import_folder(path)
                        tile_surface = item_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, int(val))
                        
                    if type == 'enemies':  # a voir apres avec val si on peut avir les autres monstres (attention changer les dossiers)
                        if val == '0':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[0])
                        if val == '1':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[1])
                        if val == '2':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[2])
                        if val == '3':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[3])
                        
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
        
    def player_setup(self,layout, change_health):
        for row_index, row in enumerate(layout): 
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1':  # le player
                    sprite = Player((x,y), change_health, self.level_data)
                    self.player.add(sprite)
                if val == '0':  # le goal
                    fin_surface = pygame.image.load('../../design/global/flag.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, fin_surface, 0)
                    self.goal.add(sprite)
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites,False):
                enemy.reverse()
        
    def horizontal_mouvement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed # on applique le mouvement horizontal
        
        for sprite in self.terrain_sprites.sprites(): # si le pesro touche un mur en x (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # si le perso touche un truc alors qu'il va a gauche
                    player.rect.left = sprite.rect.right
                    player.on_left = True 
                    self.current_x = player.rect.left 
                elif player.direction.x > 0:  # si le perso touche qqch alors qu'il va a droite
                    player.rect.right = sprite.rect.left 
                    player.on_right = True 
                    self.current_x = player.rect.right
                
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):  # on ne touche plus qqch à gauche si on va à droite ou si on passe au dessus de ce mur
            player.on_left = False 
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False 

    def vertical_mouvement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.terrain_sprites.sprites(): # si le pesro touche un mur en y (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # si le perso touche un truc alors qu'il va vers le bas
                    player.rect.bottom = sprite.rect.top 
                    player.direction.y = 0 # cela evite que la gravité augmente trop et fait passer le pero a travers les plateformes
                    player.on_ground = True  # il est bien sur le sol
                elif player.direction.y < 0:  # si le perso touche qqch alors qu'il va vers le haut
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

            # Remet chrono a 0 apres respiration
            if self.current_level == 2 and not player.on_ceiling and player.rect.top < 20:
                self.isBreathing = True
            if player.rect.top >= 64 and self.isBreathing:
                self.timeSinceLastBreath = round(time.time())
                self.isBreathing = False

        # si il touche le sol puis tombe ou saute
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False 
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False 
        
    def scroll_x(self):  # on fait en sorte que le niveau scroll si le perso avance
        player = self.player.sprite 
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        # la vitesse du pero est nulle et c'est le scroll qui remplace le mouvement du perso
        if player_x < screen_width/3 and direction_x < 0: # direction a gauche
            self.world_shift = self.level_data['speed']
            player.speed = 0 
        elif player_x > screen_width - (screen_width/3) and direction_x > 0:  # direction a droite
            self.world_shift = - self.level_data['speed']
            player.speed = 0 
        else:
            self.world_shift = 0 
            player.speed = self.level_data['speed']
        
    def check_death(self):
        if self.player.sprite.rect.top > screen_height or self.isDead:
            self.isDead = True
            self.create_overworld(self.current_level, 0)  # gerer pour mettre le game over, ou remetre au debut du niveau, ou l'overworld ? a voir
            
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win_sound.play()
            self.create_overworld(self.current_level, self.new_max_level)  # c'est la qu'il faut gerer pour mettre le dialogue
            
    def draw_back(self, surface):
        self.fond = pygame.transform.scale(self.the_fond, (screen_width, screen_height))
        self.fond = self.fond.convert()
        self.fond = surface.blit(self.fond, (0, 0))

    """
    def check_item_collisions(self): #devrait marcher 
        collided_item0 = pygame.sprite.spritecollide(self.player.sprite, self.item0_sprites, True)
        collided_item1 = pygame.sprite.spritecollide(self.player.sprite, self.item1_sprites, True)
        collided_item2 = pygame.sprite.spritecollide(self.player.sprite, self.item2_sprites, True)
        if collided_item0:
            self.change_item(self.tab_level[0])
        elif collided_item1:
            self.change_item(self.tab_level[1])
        elif collided_item2:
            self.change_item(self.tab_level[2])
    """        
    def check_item_collisions(self):
        collided_item = pygame.sprite.spritecollide(self.player.sprite, self.item_sprites, True)
        if collided_item:
            self.item_sound.play()
            for item in collided_item:
                self.change_item(self.tab_level[item.value])
    
    def check_ennemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if enemy_collisions:
            self.hit_sound.play()
            for enemy in enemy_collisions:
                self.player.sprite.get_damage()

    ### TIMER LEVEL 2 ###
    def timer(self):
        time_before = self.current_time
        self.current_time = round(time.time())
        time_left = TIME_TO_BREATH - (self.current_time - self.timeSinceLastBreath)
        time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
        if time_before != self.current_time:
            time_left = 15 - (self.current_time - self.timeSinceLastBreath)
            time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
        screen.blit(time_text, (20, 110))  # print time before death
        if time_left <= 0:
            self.isDead = True

    def run(self):
        # run the entier game/level
        # fond
        self.draw_back(self.display_surface)

        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(
            self.world_shift)  # on ne dessine pas les constraints car on ne veux pas les voir mais on veut qu'elles existent
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # item
        self.item_sprites.update(self.world_shift)
        self.item_sprites.draw(self.display_surface)

        # player sprite
        self.player.update()
        self.horizontal_mouvement_collision()
        self.vertical_mouvement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        if self.current_level == 2 and not self.isBreathing: self.timer()  # check le temps et s'il est a court des respiration
        self.check_death()
        self.check_win()

        self.check_item_collisions()
        self.check_ennemy_collisions()

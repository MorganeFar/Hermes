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
from stalactite import Stalactite
from player import Player 
from game_data import levels
from sceneryClass import Scenery

pygame.init()

### LEVEL 2 ###
screen = pygame.display.set_mode((screen_width, screen_height))
timeFont = pygame.font.Font(None, 50)
TIME_TO_BREATH = 200
###############

class Level :
    def __init__(self, current_level, surface, create_overworld, change_item, change_health, create_dialogue):
        # general setup
        self.display_surface = surface 
        self.world_shift = 0
        self.current_x = None
        
        # audio
        self.item_sound = pygame.mixer.Sound('../../audio/item.ogg')
        self.hit_sound = pygame.mixer.Sound('../../audio/hit.wav')
        self.win_sound = pygame.mixer.Sound('../../audio/victory.wav')
        self.no_time_sound = pygame.mixer.Sound('../../audio/no_time.wav')
        
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.level_data = levels[self.current_level]  # permet de le mettre en paramètre du player

        self.new_max_level = self.level_data['unlock']
        self.the_fond = pygame.image.load('../../design/niveau' + str(
            self.current_level) + '/background.png').convert_alpha()
        self.tab_level = self.level_data['items']

        # Breathing level 2
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

        # dialogues
        self.create_dialogue = create_dialogue
        self.item = ''
        self.bon_obj = self.level_data['bon_obj']
        
        # terrain setup
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')  # ici le terrain est le nom de l'image de tuile, a voir si on peut mettre plusieurs tuiles pour 1 map
        # soit coder en dur ici le blocage du niv 2

        # item setup (aussi a changer dans game_data, map test du niveau 1) item0 item1 item2 et du coup item0_sprite item1_sprite item2_sprite, en essayant de les laisser dans les fichiers design tels qu'ils sont
        item_layout = import_csv_layout(self.level_data['item'])
        self.item_sprites = self.create_tile_group(item_layout, 'item')
        
        # enemy
        enemy_layout = import_csv_layout(self.level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        
        # constraints
        constraint_layout = import_csv_layout(self.level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        
        # air pour le niveau 2
        if self.current_level == 2:
            air_layout = import_csv_layout(self.level_data['air'])
            self.air_sprites = self.create_tile_group(air_layout, 'air')
            
        # lava pour le niveau 4
        if self.current_level == 4:
            lava_layout = import_csv_layout(self.level_data['lava'])
            self.lava_sprites = self.create_tile_group(lava_layout, 'lava')
            
            stalactite_layout = import_csv_layout(self.level_data['stalactite'])
            self.stalactite_sprites = self.create_tile_group(stalactite_layout, 'stalactite')
            
            piege_layout = import_csv_layout(self.level_data['piege'])
            self.piege_sprites = self.create_tile_group(piege_layout, 'piege')
        
        # limite poiur les niveaux 2 et 4
        self.limite = pygame.Rect(0, -64, screen_width, 64)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):  # on met un numero a nos row pour mieux les distinguer et les reperer plus facilement
            for col_index, val in enumerate(row):  # pour chaque indice et chaque valeur de case
                if val != '-1':  # si il y a qqch dans la case
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
                        
                    if type == 'enemies':  # a voir apres avec val si on peut avoir les autres monstres (attention changer les dossiers)
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
                        
                    if type == 'air':
                        path = '../../design/niveau2/air'
                        air_tile_list = import_folder(path)
                        tile_surface = air_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        
                    if type == 'lava':
                        path = '../../design/niveau4/lava'
                        lava_tile_list = import_folder(path)
                        tile_surface = lava_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        
                    if type == 'stalactite':
                        if val == '0':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        if val == '1':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        if val == '2':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        
                    if type == 'piege':
                        path = '../../design/niveau4/piege'
                        piege_tile_list = import_folder(path)
                        tile_surface = piege_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, int(val))
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
        
    def player_setup(self,layout, change_health):
        for row_index, row in enumerate(layout): 
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1':  # player
                    sprite = Player((x,y), change_health, self.level_data)
                    self.player.add(sprite)
                if val == '0':  # goal
                    fin_surface = pygame.image.load('../../design/global/flag.png').convert_alpha()
                    if self.current_level == 3:
                        fin_surface = pygame.transform.flip(fin_surface, False, True)
                    sprite = StaticTile(tile_size, x, y, fin_surface, 0)
                    self.goal.add(sprite)
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
                
    def stalactite_fall(self):  # le stalactite tome quand le player arrive au piege
        collided_piege = pygame.sprite.spritecollide(self.player.sprite, self.piege_sprites, True)
        if collided_piege:
            for piege in collided_piege:
                self.id_stalactite = piege.value 
                for stalactite in self.stalactite_sprites :
                    if stalactite.value == piege.value:
                        stalactite.active(True)
                
    def horizontal_mouvement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed  # on applique le mouvement horizontal
        
        for sprite in self.terrain_sprites.sprites():  # si le pesro touche un mur en x (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # si le perso touche un truc alors qu'il va a gauche
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.on_right = False  # A RETIRER SI BESOIN
                    self.current_x = player.rect.left 
                elif player.direction.x > 0:  # si le perso touche qqch alors qu'il va a droite
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.on_left = False  # A RETIRER SI BESOIN
                    self.current_x = player.rect.right
                                                                                    #>= semble mieu fonctionner avec > ou <
        if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):  # on ne touche plus qqch à gauche si on va à droite ou si on passe au dessus de ce mur
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x < 0):
            player.on_right = False 

    def vertical_mouvement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.terrain_sprites.sprites():  # si le pesro touche un mur en y (si collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # si le perso touche un truc alors qu'il va vers le bas
                    player.rect.bottom = sprite.rect.top 
                    player.direction.y = 0  # cela evite que la gravité augmente trop et fait passer le pero a travers les plateformes
                    player.on_ground = True  # il est bien sur le sol
                    player.on_ceiling = False  # A RETIRER SI BESOIN
                elif player.direction.y < 0:  # si le perso touche qqch alors qu'il va vers le haut
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    player.on_ground = False  # A RETIRER SI BESOIN

            # Remet chrono a 0 apres respiration
            if self.current_level == 2 and player.rect.top < 20:
                self.isBreathing = True
            if player.rect.top >= 64 and self.isBreathing:
                self.timeSinceLastBreath = round(time.time())
                self.isBreathing = False

        # si il touche le sol puis tombe ou saute
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False 
        
    def plafond_collison_niv24(self):
        player = self.player.sprite
        if self.limite.colliderect(player.rect):
            print(f'limite :{self.limite.bottom}')
            print(f'player top :{player.rect.top}')
            player.rect.top = self.limite.bottom
            #player.direction.y = 0
            print(player.on_right)
            print(player.on_left)
            print(player.direction.x)
            player.on_ceiling = True
            player.on_ground = False

    def scroll_x(self):  # on fait en sorte que le niveau scroll si le perso avance
        player = self.player.sprite 
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        # la vitesse du pero est nulle et c'est le scroll qui remplace le mouvement du perso
        if player_x < screen_width/3 and direction_x < 0:  # direction a gauche
            self.world_shift = self.level_data['speed']
            player.speed = 0 
        elif player_x > screen_width - (screen_width/3) and direction_x > 0:  # direction a droite
            self.world_shift = - self.level_data['speed']
            player.speed = 0 
        else:
            self.world_shift = 0 
            player.speed = self.level_data['speed']
        
    def check_death(self):
        if self.player.sprite.rect.top > screen_height+2000 or self.isDead:
            self.isDead = True
            self.create_overworld(self.current_level, 0, 'perdu')  # gerer pour mettre le game over, ou remetre au debut du niveau, ou l'overworld ? a voir
        elif self.player.sprite.rect.top < -2000 or self.isDead:
            self.isDead = True
            self.create_overworld(self.current_level, 0, 'perdu')
            
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            final = 'perdu'
            if self.item == self.bon_obj:  # verifie si le dernier item est le bon objet
                final = 'gagne'
            self.win_sound.play()
            self.create_dialogue(self.current_level)  # on cree un dialogue
            if final == 'gagne': 
                self.create_overworld(self.current_level, self.new_max_level, final)
            else:
                self.create_overworld(self.current_level, self.current_level, final)
            
    def draw_back(self, surface):
        self.fond = pygame.transform.scale(self.the_fond, (screen_width, screen_height))
        self.fond = self.fond.convert()
        self.fond = surface.blit(self.fond, (0, 0))
       
    def check_item_collisions(self):
        collided_item = pygame.sprite.spritecollide(self.player.sprite, self.item_sprites, True)
        if collided_item:
            self.item_sound.play()
            for item in collided_item:
                #print(f'item : {self.item}')
                #print(f'change item : {self.change_item}')
                self.change_item(self.tab_level[item.value])
                self.item = self.tab_level[item.value]
    
    def check_ennemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if enemy_collisions:
            self.hit_sound.play()
            for enemy in enemy_collisions:
                self.player.sprite.get_damage()
                
    def check_stalactite_collision(self):
        stalactite_collisions = pygame.sprite.spritecollide(self.player.sprite, self.stalactite_sprites, False)
        if stalactite_collisions:
            self.hit_sound.play()
            for stalactite in stalactite_collisions:
                self.player.sprite.get_damage()

    ### TIMER LEVEL 2 ###
    def timer(self):
        time_before = self.current_time
        self.current_time = round(time.time())
        time_left = TIME_TO_BREATH - (self.current_time - self.timeSinceLastBreath)
        time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
        if time_before != self.current_time:
            time_left = TIME_TO_BREATH - (self.current_time - self.timeSinceLastBreath)
            time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
            if time_left <= 5:
                self.no_time_sound.play()
        screen.blit(time_text, (20, 110))  # print time before death
        if time_left <= 0:
            self.isDead = True

    def run(self):
        # run the entier game/level
        # fond
        self.draw_back(self.display_surface)
        
        # air
        if self.current_level == 2:
            self.air_sprites.draw(self.display_surface)
            self.air_sprites.update(self.world_shift)
            
        # lava
        if self.current_level == 4:
            self.lava_sprites.draw(self.display_surface)
            self.lava_sprites.update(self.world_shift)

        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)  # on ne dessine pas les constraints car on ne veux pas les voir mais on veut qu'elles existent
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        # stalactite
        if self.current_level == 4:
            self.stalactite_sprites.update(self.world_shift)
            self.piege_sprites.update(self.world_shift)  # on ne dessine pas les pieges car on ne veux pas les voir mais on veut qu'elles existent
            self.stalactite_fall()
            self.stalactite_sprites.draw(self.display_surface)

        # item
        self.item_sprites.update(self.world_shift)
        self.item_sprites.draw(self.display_surface)

        # player sprite
        self.player.update()
        self.horizontal_mouvement_collision()
        self.vertical_mouvement_collision()
        if (self.current_level == 2) or (self.current_level == 4): self.plafond_collison_niv24()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        if self.current_level == 2 and not self.isBreathing: self.timer()  # check le temps et s'il est a court des respiration
        self.check_death()
        self.check_win()

        self.check_item_collisions()
        self.check_ennemy_collisions()
        if self.current_level == 4:
            self.check_stalactite_collision()

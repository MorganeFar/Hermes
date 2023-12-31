# -*- coding: utf-8 -*-
"""
level
"""

import pygame, sys
import time
sys.path.append('../')
from support import import_csv_layout, import_cut_graphic, import_folder
from settings import tile_size, screen_height, screen_width 
from tiles import Tile, StaticTile, AnimatedTile, TileLevel5
from enemy import Enemy 
from stalactite import Stalactite
from player import Player 
from game_data import levels
from sceneryClass import Scenery

pygame.init()

### LEVEL 2 ###
screen = pygame.display.set_mode((screen_width, screen_height))
timeFont = pygame.font.Font(None, 50)
TIME_TO_BREATH = 20

class Level :
    def __init__(self, current_level, surface, create_overworld, change_item, change_health, create_dialogue):
        # general setup
        self.display_surface = surface 
        self.world_shift = 0
        self.current_x = None
        self.tile_size = tile_size
        
        # audio
        self.item_sound = pygame.mixer.Sound('../../audio/item.ogg')
        self.hit_sound = pygame.mixer.Sound('../../audio/hit.wav')
        self.win_sound = pygame.mixer.Sound('../../audio/victory.wav')
        self.no_time_sound = pygame.mixer.Sound('../../audio/no_time.wav')
        
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.level_data = levels[self.current_level]  # permet de le mettre en paramètre du player
        
        # general setup suite
        if current_level == 5: 
            self.world_shift = self.level_data['speed']
        self.new_max_level = self.level_data['unlock']
        
        # le fond
        self.x_fond = 0
        self.y_fond = 0
        # le fond paralaxe pour le niveau 5
        if self.current_level == 5:
            self.fond1 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background1.png').convert_alpha(), (screen_width, screen_height))
            self.fond2 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background2.png').convert_alpha(), (screen_width, screen_height))
            self.fond3 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background3.png').convert_alpha(), (screen_width, screen_height))
            self.fond4 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background4.png').convert_alpha(), (screen_width, screen_height))
            self.fond5 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background5.png').convert_alpha(), (screen_width, screen_height))
            self.fond6 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background6.png').convert_alpha(), (screen_width, screen_height))
            self.fond7 = pygame.transform.scale(pygame.image.load('../../design/niveau5/background7.png').convert_alpha(), (screen_width, screen_height))
            self.fond1 = pygame.transform.scale(self.fond1, (screen_width, screen_height)).convert()
            self.fond2 = pygame.transform.scale(self.fond2, (screen_width, screen_height)).convert()
            self.fond3 = pygame.transform.scale(self.fond3, (screen_width, screen_height)).convert()
            self.fond4 = pygame.transform.scale(self.fond4, (screen_width, screen_height)).convert()
            self.fond5 = pygame.transform.scale(self.fond5, (screen_width, screen_height)).convert()
            self.fond6 = pygame.transform.scale(self.fond6, (screen_width, screen_height)).convert()
            self.fond7 = pygame.transform.scale(self.fond7, (screen_width, screen_height)).convert()
        # le fond des autres niveaux
        else:
            self.the_fond = pygame.image.load('../../design/niveau' + str(self.current_level) + '/background.png').convert_alpha()
        
        if self.current_level !=5:
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

        # replacement pour le niveau 5
        self.replace = False 
        self.taille = 11664 - 704  # taille complete du niveau - taille de l'ecran (en y)

        # monsters
        if self.current_level !=5:
            self.tab_monsters = self.level_data['monsters']

        # player
        player_layout = import_csv_layout(self.level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        self.isDead = False
        self.isBreathing = True

        # user interface
        if self.current_level !=5:
            self.change_item = change_item

        # dialogues
        self.create_dialogue = create_dialogue
        self.item = ''
        if self.current_level !=5:
            self.bon_obj = self.level_data['bon_obj']
        
        # terrain setup
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')  # ici le terrain est le nom de l'image de tuile

        if self.current_level != 5:
            # item setup 
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
        
        # limite pour le niveau 5
        if self.current_level == 5:
            death_line_layout = import_csv_layout(self.level_data['death_line'])
            self.death_line = self.create_tile_group(death_line_layout, 'death_line')
            
        # hera pour le niveau 5
        self.hera = pygame.image.load("../../design/niveau5/hera_2.png").convert_alpha()
        self.hera = pygame.transform.scale(self.hera, (47.5, 110))
        self.hera_x = screen_width * (1/2)
        self.hera_y = screen_height * (21/24)
        self.hera_rect = self.hera.get_rect(topleft=(self.hera_x, self.hera_y))
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):  # on met un numero a nos row pour mieux les distinguer et les reperer plus facilement
            for col_index, val in enumerate(row):  # pour chaque indice et chaque valeur de case
                if val != '-1': # si il y a qqch dans la case
                    if self.current_level == 5:
                        self.tile_size = 72
                    x = col_index * self.tile_size  
                    y = row_index * self.tile_size 
                    
                    if type == 'terrain':
                        # terrain_tile_list = import_cut_graphic('../../niveaux/nv_1_apollon/tiles/midTile_1.png')
                        path = '../../design/niveau' + str(self.current_level) + '/tiles'
                        terrain_tile_list = import_folder(path)
                        tile_surface = terrain_tile_list[int(val)]
                        
                        if self.current_level !=5:
                            sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        else: sprite = TileLevel5(self.tile_size, x, y, tile_surface, val)
                        
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
                        
                    if type == 'death_line' :
                        path = '../../design/global'
                        death_line_tile_list = import_folder(path)
                        tile_surface = death_line_tile_list[int(val)]
                        sprite = TileLevel5(self.tile_size, x, y, tile_surface, val)
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
        
    def player_setup(self,layout, change_health):
        for row_index, row in enumerate(layout): 
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1':  # le player
                    if self.current_level == 5:
                        sprite = Player((x, screen_height*(5/6)), change_health, self.level_data)  #y - self.taille
                    else:
                        sprite = Player((x,y), change_health, self.level_data)
                    self.player.add(sprite)
                if val == '0':  # le goal
                    fin_surface = pygame.image.load('../../design/global/flag.png').convert_alpha()
                    if self.current_level == 3:
                        fin_surface = pygame.transform.flip(fin_surface, False, True)
                    if self.current_level == 5:
                        sprite = TileLevel5(tile_size, x +72, y - self.taille, fin_surface, 0)  # - self.taille + (1.9)*704
                    else:
                        sprite = StaticTile(tile_size, x, y, fin_surface, 0)
                    self.goal.add(sprite)
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
                
    def stalactite_fall(self):  # le stalactite tombe quand le player arrive au piege
        collided_piege = pygame.sprite.spritecollide(self.player.sprite, self.piege_sprites, True)
        if collided_piege:
            for piege in collided_piege:
                self.id_stalactite = piege.value 
                for stalactite in self.stalactite_sprites :
                    if stalactite.value == piege.value:
                        stalactite.active(True)
                
    def horizontal_mouvement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed # on applique le mouvement horizontal
        
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

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):  # on ne touche plus qqch à gauche si on va à droite ou si on passe au dessus de ce mur
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
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
                    #print("ground")
                elif player.direction.y < 0:  # si le perso touche qqch alors qu'il va vers le haut
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    player.on_ground = False  # A RETIRER SI BESOIN
                    #print("ceiling")

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
            player.rect.top = self.limite.bottom
            player.apply_gravity()  # evite qu'Hermes "colle" au plafond
            player.direction.y = 0
            player.on_ceiling = True
            print("plafond collision")
            player.on_ground = False
        
    def scroll_x(self):  # on fait en sorte que le niveau scroll si le perso avance
        player = self.player.sprite 
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        # la vitesse du pero est nulle et c'est le scroll qui remplace le mouvement du perso
        if player_x < screen_width/3 and direction_x < 0:  # direction a gauche
            self.world_shift = self.level_data['speed']
            player.speed = 0 
            self.x_fond += 1.5
        elif player_x > screen_width - (screen_width/3) and direction_x > 0:  # direction a droite
            self.world_shift = - self.level_data['speed']
            player.speed = 0 
            self.x_fond -= 1.5
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
            
    def check_death_niv5(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.death_line, False):
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
                
    def check_win_niv5(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win_sound.play()
            self.create_dialogue(6)
            self.create_overworld(self.current_level, self.new_max_level, 'gagne')
            
    def draw_back(self, surface):
        if self.current_level == 5:
            self.fondA = surface.blit(self.fond1, (0, self.y_fond))
            self.fondB = surface.blit(self.fond2, (0, self.y_fond - screen_height))
            self.fondC = surface.blit(self.fond3, (0, self.y_fond - 2*screen_height))
            self.fondD = surface.blit(self.fond4, (0, self.y_fond - 3*screen_height))
            self.fondE = surface.blit(self.fond5, (0, self.y_fond - 4*screen_height))
            self.fondF = surface.blit(self.fond6, (0, self.y_fond - 5*screen_height))
            self.fondG = surface.blit(self.fond7, (0, self.y_fond - 6*screen_height))
        else:
            self.fond = pygame.transform.scale(self.the_fond, (screen_width, screen_height))
            self.fond = self.fond.convert()
            if (self.x_fond > screen_width) or (self.x_fond < -screen_width):
                self.x_fond = 0
            self.fond0 = surface.blit(pygame.transform.flip(self.fond, True, False), (self.x_fond, 0))  # background
            self.fond1 = surface.blit(self.fond, (self.x_fond - screen_width, 0))
            self.fond2 = surface.blit(self.fond, (self.x_fond + screen_width, 0))  # terrain

       
    def check_item_collisions(self):
        collided_item = pygame.sprite.spritecollide(self.player.sprite, self.item_sprites, True)
        if collided_item:
            self.item_sound.play()
            for item in collided_item:
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
                
    def check_collision_niv5(self):
        objet_collisions = pygame.sprite.spritecollide(self.player.sprite, self.terrain_sprites, False)
        if objet_collisions:
            self.hit_sound.play()
            for objet in objet_collisions:
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
            
    # hera pour le niveau 5
    def hera_ai(self):
        # on fait en sorte que hera bouge en suivant le joueur
        player = self.player.sprite 
        player_x = player.rect.centerx
        if self.hera_x < player_x:
            self.hera_x += 5
        if self.hera_x > player_x:
            self.hera_x -= 5
        self.hera_rect = self.hera.get_rect(topleft=(self.hera_x, self.hera_y))

    def run(self): #a refaire niv 5 
        # run the entier game/level
        if self.current_level !=5:
            # fond
            self.draw_back(self.display_surface)
            
            #air
            if self.current_level == 2 :
                self.air_sprites.draw(self.display_surface)
                self.air_sprites.update(self.world_shift)
                
            #lava
            if self.current_level == 4 :
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
            
            #stalactite
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
        else: 
            if not self.replace:
                self.terrain_sprites.update(self.taille)
                self.death_line.update(self.taille)
                self.replace = True
                #on cree le dialogue du debut 
                self.create_dialogue(5)
            
            # fond
            self.draw_back(self.display_surface)
            self.y_fond += 1.5
            
            # terrain
            self.terrain_sprites.draw(self.display_surface)
            self.terrain_sprites.update(-self.world_shift)
            
            #death line
            self.death_line.update(-self.world_shift)
            
            #hera
            self.display_surface.blit(self.hera, (self.hera_x, self.hera_y))
            self.hera_ai()
            
            # player sprite
            self.player.update()
            self.player.draw(self.display_surface)
            self.goal.update(-self.world_shift)
            self.goal.draw(self.display_surface)
            self.check_death_niv5()
            self.check_win_niv5()
            
            self.check_collision_niv5()


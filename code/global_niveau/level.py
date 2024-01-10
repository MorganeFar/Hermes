# -*- coding: utf-8 -*-
"""
level
"""
# ---------------- IMPORTATIONS ----------------

import pygame, sys
import time
sys.path.append('../')
from support import import_csv_layout, import_folder
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, TileLevel5
from enemy import Enemy 
from stalactite import Stalactite
from player import Player 
from game_data import levels

# -----------------------------------------------

pygame.init()

# Informations specifiques pour le niveau 5 
TAILLE_NIVEAU_COMPLET = 11664
TAILLE_ECRAN = 704

# -------------- NIVEAU 2 --------------
screen = pygame.display.set_mode((screen_width, screen_height))
timeFont = pygame.font.Font(None, 50)   # Font pour afficher le chronometre
TIME_TO_BREATH = 20     # Temps de respiration
# --------------------------------------

class Level:
    def __init__(self, current_level, surface, create_overworld, change_item, change_health, create_dialogue):
        # General setup
        self.display_surface = surface 
        self.world_shift = 0 # Le déplacement du monde 
        self.current_x = None # La position actuelle du joueur
        self.tile_size = tile_size      # Taille des blocs
        
        # Audio
        self.item_sound = pygame.mixer.Sound('../../audio/item.ogg')
        self.hit_sound = pygame.mixer.Sound('../../audio/hit.wav')
        self.win_sound = pygame.mixer.Sound('../../audio/victory.wav')
        self.no_time_sound = pygame.mixer.Sound('../../audio/no_time.wav')
        
        # Connexion avec la carte
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.level_data = levels[self.current_level]  # Information relative au niveau et au joueur
        
        # General setup
        if current_level == 5: 
            self.world_shift = self.level_data['speed']

        self.new_max_level = self.level_data['unlock']      # Prochain niveau debloque
        
        # ---- FOND ----
        # Debut en haut a gauche de la fenetre
        self.x_fond = 0
        self.y_fond = 0

        # Fond paralaxe pour le niveau 5
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

        # Fond des autres niveaux
        else:
            self.the_fond = pygame.image.load('../../design/niveau' + str(self.current_level) + '/background.png').convert_alpha()
        
        if self.current_level !=5:
            self.tab_level = self.level_data['items'] # Tableau avec les différents items du niveau 

        # Respiration niveau 2
        if self.current_level == 2:
            self.current_time = 0
            self.timeSinceLastBreath = round(time.time())  # Recupere le nombre de secondes depuis epoch
            # cf. epoch = 'moment ou le temps commence' => 1 janvier 1970 00:00:00
            self.timer()  # Lance le chrono

        # Replacement des positions des layout du niveau 5 pour correspondre a la position de la camera
        self.replace = False 
        self.taille = TAILLE_NIVEAU_COMPLET - TAILLE_ECRAN  # En hauteur (en y)

        # Monstres
        if self.current_level != 5:  # Pas de monstre dans le niveau 5 seulement
            self.tab_monsters = self.level_data['monsters']

        # Joueur
        player_layout = import_csv_layout(self.level_data['player'])
        self.player = pygame.sprite.GroupSingle()   # Creation d'un groupe de sprite pour le joueur
        self.goal = pygame.sprite.GroupSingle()     # Groupe de sprite pour l'arrive du joueur
        self.player_setup(player_layout, change_health)
        self.isDead = False     # Le joueur commence vivant
        self.isBreathing = True  # Le joueur prend un respiration avant de commencer le niveau 2

        # Interface utilisateur
        if self.current_level != 5:     # Pas d'objet a collecter dans le niveau 5
            self.change_item = change_item

        # Dialogues
        self.create_dialogue = create_dialogue
        self.item = ''  # Au depart le joueur n'a recupere aucun objet
        if self.current_level != 5:
            self.bon_obj = self.level_data['bon_obj']     # L'objet recupere est celui attendu
        
        # Terrain setup
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        # Ici le terrain est le nom de l'image de tuile
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        if self.current_level != 5:
            # Objet setup
            item_layout = import_csv_layout(self.level_data['item'])
            self.item_sprites = self.create_tile_group(item_layout, 'item')
            
            # Monstres
            enemy_layout = import_csv_layout(self.level_data['enemies'])
            self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
            
            # Constraints
            constraint_layout = import_csv_layout(self.level_data['constraints'])
            self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
            
        # Bulle d'air pour le niveau 2
        if self.current_level == 2:
            air_layout = import_csv_layout(self.level_data['air'])
            self.air_sprites = self.create_tile_group(air_layout, 'air')
            
        # Lave du niveau 4
        if self.current_level == 4:
            lava_layout = import_csv_layout(self.level_data['lava'])
            self.lava_sprites = self.create_tile_group(lava_layout, 'lava')

            # Pieges niveau 4
                # Le piege qui met des degats au joueur
            stalactite_layout = import_csv_layout(self.level_data['stalactite'])
            self.stalactite_sprites = self.create_tile_group(stalactite_layout, 'stalactite')
                # Ce qui active les pieges 
            piege_layout = import_csv_layout(self.level_data['piege'])
            self.piege_sprites = self.create_tile_group(piege_layout, 'piege')
        
        # Limite au plafond pour les niveaux 2 et 4
        self.limite = pygame.Rect(0, -64, screen_width, 64)
        
        # Limite pour le niveau 5
        if self.current_level == 5:
            death_line_layout = import_csv_layout(self.level_data['death_line'])
            self.death_line = self.create_tile_group(death_line_layout, 'death_line')
            
        # Creation de Hera pour le niveau 5
        self.hera = pygame.image.load("../../design/niveau5/hera_2.png").convert_alpha()
        self.hera = pygame.transform.scale(self.hera, (47.5, 110))
        self.hera_x = screen_width * (1/2)
        self.hera_y = screen_height * (21/24)
        self.hera_rect = self.hera.get_rect(topleft=(self.hera_x, self.hera_y))

    # Creation des elements sur le terrain
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        # Numerotation des lignes pour mieux les distinguer et les reperer plus facilement
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):  # Parcours chaque indice et chaque valeur de case
                if val != '-1':  # s'il y a quelque chose dans la case

                    if self.current_level == 5:
                        self.tile_size = 72     # Taille des briques differentes pour le niveau 5
                    # Coordonnees de l'element avec mise a l'echelle de la dimension
                    x = col_index * self.tile_size  
                    y = row_index * self.tile_size 
                    
                    if type == 'terrain':  # Place la brique
                        path = '../../design/niveau' + str(self.current_level) + '/tiles'
                        terrain_tile_list = import_folder(path)
                        tile_surface = terrain_tile_list[int(val)]
                        
                        if self.current_level != 5:
                            sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        else: sprite = TileLevel5(self.tile_size, x, y, tile_surface, val)
                        
                    if type == 'item':  # Place les objets
                        path = '../../design/niveau' + str(self.current_level) + '/object'
                        item_tile_list = import_folder(path)
                        tile_surface = item_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, int(val))
                        
                    if type == 'enemies':  # Place les monstres
                        if val == '0':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[0])
                        if val == '1':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[1])
                        if val == '2':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[2])
                        if val == '3':
                            sprite = Enemy(tile_size, x, y, self.tab_monsters[3])
                        
                    if type == 'constraints':   # Place la limite du terrain
                        sprite = Tile(tile_size, x, y)
                        
                    if type == 'air':   # Place la bulle d'air du niveau 2
                        path = '../../design/niveau2/air'
                        air_tile_list = import_folder(path)
                        tile_surface = air_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        
                    if type == 'lava':  # Place la lave du niveau 4
                        path = '../../design/niveau4/lava'
                        lava_tile_list = import_folder(path)
                        tile_surface = lava_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, 0)
                        
                    if type == 'stalactite':    # Place les stalactites du niveau 4
                        if val == '0':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        if val == '1':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        if val == '2':
                            sprite = Stalactite(tile_size, x, y, '../../design/niveau4/stalactite', False, int(val))
                        
                    if type == 'piege':  # Place les pieges
                        path = '../../design/niveau4/piege'
                        piege_tile_list = import_folder(path)
                        tile_surface = piege_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, int(val))
                        
                    if type == 'death_line': # Place le ligne de game over du niveau 5 (cas ou le joueur rate le drapeau)
                        path = '../../design/global'
                        death_line_tile_list = import_folder(path)
                        tile_surface = death_line_tile_list[int(val)]
                        sprite = TileLevel5(self.tile_size, x, y, tile_surface, val)
                        
                    sprite_group.add(sprite) # Ajout des sprites au groupe 
                    
        return sprite_group

    # Mise en place du joueur dans le niveau
    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout): 
            for col_index, val in enumerate(row):
                # Coordonnees des elements lies au joueur
                x = col_index * tile_size
                y = row_index * tile_size

                if val == '1':  # Joueur
                    if self.current_level == 5:
                        # Place le joueur en bas au centre de la fenetre, mis manuellement 
                        sprite = Player((x, screen_height*(5/6)), change_health, self.level_data)
                    else:
                        # Place le joueur en bas a gauche de la fenetre (endroit predetermine dans le layout)
                        sprite = Player((x,y), change_health, self.level_data)
                    self.player.add(sprite)

                if val == '0':  # Place l'arrivee du niveau
                    fin_surface = pygame.image.load('../../design/global/flag.png').convert_alpha()
                    if self.current_level == 3:
                        # Drapeau retourne pour la gravite inversee
                        fin_surface = pygame.transform.flip(fin_surface, False, True)
                    if self.current_level == 5:
                        # Drapeau centre, mis manuellement 
                        sprite = TileLevel5(tile_size, x + 72, y - self.taille, fin_surface, 0)  # - self.taille + (1.9)*704
                    else:
                        # Drapeau place a la fin du niveau classiquement
                        sprite = StaticTile(tile_size, x, y, fin_surface, 0)
                    self.goal.add(sprite)

    # Collision des monstres avec leur limite
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()  # Le monstre part dans le sens inverse

    # Stalactite tombe quand le joueur arrive au piege
    def stalactite_fall(self):
        # Le joueur entre dans le piege (ce qui le declanche)
        collided_piege = pygame.sprite.spritecollide(self.player.sprite, self.piege_sprites, True)
        if collided_piege:
            for piege in collided_piege:
                self.id_stalactite = piege.value 
                for stalactite in self.stalactite_sprites:
                    # Le stalactite lie au piege tombe
                    if stalactite.value == piege.value:
                        stalactite.active(True)

    # Collision horizontale du joueur avec une brique (le terrain)
    def horizontal_mouvement_collision(self):
        player = self.player.sprite     # Recupere le joueur
        player.rect.x += player.direction.x * player.speed  # Applique mouvement horizontal
        
        for sprite in self.terrain_sprites.sprites():  # Si le joueur touche un mur en x (collision avec le terrain)
            if sprite.rect.colliderect(player.rect):

                if player.direction.x < 0:  # Le joueur touche un bloc en allant a gauche
                    player.rect.left = sprite.rect.right    # Replacement du joueur a la limite du bloc
                    player.on_left = False
                    player.on_right = False
                    self.current_x = player.rect.left

                elif player.direction.x > 0:  # Le joueur touche un bloc en allant a droite
                    player.rect.right = sprite.rect.left    # Replacement a la limite du bloc
                    player.on_right = True
                    player.on_left = False
                    self.current_x = player.rect.right
                else:  # Le joueur ne se deplace pas a droite ni a gauche
                    player.on_left = False
                    player.on_right = False

        # Le joueur ne touche plus de bloc a gauche s'il va a droite ou s'il passe au dessus du mur
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        # Idem dans l'autre sens
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False 

    # Collision verticale entre le joueur et un bloc
    def vertical_mouvement_collision(self):
        player = self.player.sprite     # Recupere le joueur
        player.apply_gravity()      # Applique la gravite
        for sprite in self.terrain_sprites.sprites():  # Si le joueur touche un mur en y (collision avec le terrain)
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # Le joueur touche un bloc alors qu'il va vers le bas
                    player.rect.bottom = sprite.rect.top    # Place le joueur a la limite du bloc
                    # Evite que la gravite augmente trop et fasse passer le joueur a travers les plateformes
                    player.direction.y = 0
                    player.on_ground = True  # Le joueur est bien sur le sol
                    player.on_ceiling = False

                elif player.direction.y < 0:  # Si le joueur touche un bloc alors qu'il va vers le haut
                    player.rect.top = sprite.rect.bottom    # Place le joueur a la limite du bloc
                    player.direction.y = 0
                    player.on_ceiling = True
                    player.on_ground = False

                else:
                    player.rect.bottom = sprite.rect.bottom

            # Remet chrono a 0 apres une respiration
            if self.current_level == 2 and player.rect.top < 20:  # Le joueur est dans une bulle d'air
                self.isBreathing = True     # Il respire
            if player.rect.top >= 64 and self.isBreathing:      # Le joueur est sortie de la bulle d'air
                self.timeSinceLastBreath = round(time.time())   # Temps a la derniere respiration
                self.isBreathing = False

        # Si le joueur touche le sol puis tombe ou saute alors il ne touche plus le sol
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False 
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False 

    # Limite de plafond pour les niveaux 2 et 4
    def plafond_collison_niv24(self):
        player = self.player.sprite
        if self.limite.colliderect(player.rect):    # Le joueur entre en collision avec la limite
            player.rect.top = self.limite.bottom    # Il est replacer sous la limite
            player.apply_gravity()  # Evite que le joueur "colle" au plafond
            player.direction.y = 0  # Ne monte plus
            player.on_ceiling = True
            player.on_ground = False

    # Fait en sorte que le niveau scroll si le joueur avance
    def scroll_x(self):
        player = self.player.sprite 
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # Lorsque le joueur atteint un certain point a droite ou a gauche
        # La vitesse du joueur est nulle et c'est le scroll qui remplace le mouvement du perso
        if player_x < screen_width/3 and direction_x < 0:  # Direction a gauche
            self.world_shift = self.level_data['speed']
            player.speed = 0 
            self.x_fond += 1.5
        elif player_x > screen_width - (screen_width/3) and direction_x > 0:  # Direction a droite
            self.world_shift = - self.level_data['speed']
            player.speed = 0 
            self.x_fond -= 1.5
        else:
            self.world_shift = 0 
            player.speed = self.level_data['speed']

    # Verifie l'etat du joueur (mort)
    def check_death(self):
        # S'il tombe dans le niveau 3 il meurt
        if self.player.sprite.rect.top > screen_height+2000 or self.isDead and self.current_level == 3:
            self.isDead = True
            self.create_overworld(self.current_level, 0, 'perdu')  # Mise a jour de l'etat du jeu
        # S'il tombe il meurt
        elif self.player.sprite.rect.top < -2000 or self.isDead:
            self.isDead = True
            self.create_overworld(self.current_level, 0, 'perdu')

    # Verification etat du joueur niveau 5 (ne peut pas tomber)
    def check_death_niv5(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.death_line, False):
            self.isDead = True
            self.create_overworld(self.current_level, 0, 'perdu')

    # Verification de l'etat du joueur (gagner)
    def check_win(self):
        # Touche le drapeau
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            final = 'perdu'
            if self.item == self.bon_obj:  # Verifie si l'objet du sac est le bon objet
                final = 'gagne'
            self.win_sound.play()
            self.create_dialogue(self.current_level)  # Creation d'un dialogue en consequence

            # Mise a jour de la carte
            if final == 'gagne':
                self.create_overworld(self.current_level, self.new_max_level, final)
            else:
                self.create_overworld(self.current_level, self.current_level, final)

    # Verifie l'etat du joueur au niveau 5 (gagne)
    def check_win_niv5(self):
        # Touche le drapeau
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win_sound.play()
            self.create_dialogue(6)  # Dialogue de fin avec Zeus 
            self.create_overworld(self.current_level, self.new_max_level, 'gagne')

    # Gestion du fond parallaxe
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
            self.fond0 = surface.blit(self.fond, (self.x_fond, 0))
            self.fond1 = surface.blit(self.fond, (self.x_fond - screen_width, 0))
            self.fond2 = surface.blit(self.fond, (self.x_fond + screen_width, 0))


    # Verifie la collecte d'objets
    def check_item_collisions(self):
        # Le joueur touche un objet
        collided_item = pygame.sprite.spritecollide(self.player.sprite, self.item_sprites, True)
        if collided_item:
            # L'objet est collecte
            self.item_sound.play()
            for item in collided_item:
                self.change_item(self.tab_level[item.value])
                self.item = self.tab_level[item.value]

    # Verifie la collision entre le joueur et les monstres
    def check_ennemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if enemy_collisions:    # Le joueur touche un monstre
            self.hit_sound.play()
            for enemy in enemy_collisions:
                self.player.sprite.get_damage()     # Le joueur perd une vie

    # Verifie la collision entre le joueur et les stalactite
    def check_stalactite_collision(self):
        stalactite_collisions = pygame.sprite.spritecollide(self.player.sprite, self.stalactite_sprites, False)
        if stalactite_collisions:  # Le joueur est touche
            self.hit_sound.play()
            for stalactite in stalactite_collisions:
                self.player.sprite.get_damage()     # Il perde une vie

     # Verifie la collision entre le joueur et les blocs de terrain du niveau 5
    def check_collision_niv5(self):
        objet_collisions = pygame.sprite.spritecollide(self.player.sprite, self.terrain_sprites, False)
        if objet_collisions:
            self.hit_sound.play()
            for objet in objet_collisions:
                self.player.sprite.get_damage()     # Il perde une vie

    # Met un timer pour le niveau 2
    def timer(self):
        time_before = self.current_time
        self.current_time = round(time.time())
        time_left = TIME_TO_BREATH - (self.current_time - self.timeSinceLastBreath)
        time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
        if time_before != self.current_time:
            time_left = TIME_TO_BREATH - (self.current_time - self.timeSinceLastBreath)
            time_text = timeFont.render(f"{time_left}", False, (0, 0, 0))
            if time_left <= 5:
                self.no_time_sound.play() # Si le temps est inferieur a 5 il y a un son d'avertissement 
        screen.blit(time_text, (20, 110))  # Print time before death
        if time_left <= 0:
            self.isDead = True
            
    # Mise en place d'Hera pour le niveau 5
    def hera_ai(self):
        # Fait en sorte que hera bouge en suivant le joueur
        player = self.player.sprite 
        player_x = player.rect.centerx
        if self.hera_x < player_x:
            self.hera_x += 5
        if self.hera_x > player_x:
            self.hera_x -= 5
        self.hera_rect = self.hera.get_rect(topleft=(self.hera_x, self.hera_y))

    def run(self):
        # Run the entier game/level
        if self.current_level !=5:
            # Fond
            self.draw_back(self.display_surface)
            
            # Air
            if self.current_level == 2 :
                self.air_sprites.draw(self.display_surface)
                self.air_sprites.update(self.world_shift)
                
            # Lave
            if self.current_level == 4 :
                self.lava_sprites.draw(self.display_surface)
                self.lava_sprites.update(self.world_shift)
    
            # Terrain
            self.terrain_sprites.draw(self.display_surface)
            self.terrain_sprites.update(self.world_shift)
    
            # Ennemies
            self.enemy_sprites.update(self.world_shift)
            self.constraint_sprites.update(self.world_shift)  # on ne dessine pas les constraints car on ne veux pas les voir mais on veut qu'elles existent
            self.enemy_collision_reverse()
            self.enemy_sprites.draw(self.display_surface)
            
            # Stalactite
            if self.current_level == 4:
                self.stalactite_sprites.update(self.world_shift)
                self.piege_sprites.update(self.world_shift)  # on ne dessine pas les pieges car on ne veux pas les voir mais on veut qu'elles existent
                self.stalactite_fall()
                self.stalactite_sprites.draw(self.display_surface)
    
            # Item
            self.item_sprites.update(self.world_shift)
            self.item_sprites.draw(self.display_surface)
    
            # Player sprite
            self.player.update()
            if (self.current_level == 2) or (self.current_level == 4): self.plafond_collison_niv24()
            self.scroll_x()
            self.player.draw(self.display_surface)
            self.horizontal_mouvement_collision()
            self.vertical_mouvement_collision()
            self.goal.update(self.world_shift)
            self.goal.draw(self.display_surface)
            if self.current_level == 2 and not self.isBreathing: self.timer()  # check le temps et s'il est a court des respiration
            self.check_death()
            self.check_win()

            # Verifie les collisions 
            self.check_item_collisions()
            self.check_ennemy_collisions()
            if self.current_level == 4:
                self.check_stalactite_collision()
        else: 
            if not self.replace: # A la creation du niveau on decale les layout pour correspondre a la position de la camera
                self.terrain_sprites.update(self.taille)
                self.death_line.update(self.taille)
                self.replace = True
                # On cree le dialogue du debut 
                self.create_dialogue(5)
            
            # Fond
            self.draw_back(self.display_surface)
            self.y_fond += 1.5
            
            # Terrain
            self.terrain_sprites.draw(self.display_surface)
            self.terrain_sprites.update(-self.world_shift)
            
            # Death line
            self.death_line.update(-self.world_shift)
            
            # Hera
            self.display_surface.blit(self.hera, (self.hera_x, self.hera_y))
            self.hera_ai()
            
            # Player sprite
            self.player.update()
            self.player.draw(self.display_surface)
            self.goal.update(-self.world_shift)
            self.goal.draw(self.display_surface)
            self.check_death_niv5()
            self.check_win_niv5()

            # Verifie les collisions 
            self.check_collision_niv5()


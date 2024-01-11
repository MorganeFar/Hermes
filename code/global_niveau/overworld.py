# -*- coding: utf-8 -*-
"""
overworld 
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from game_data import levels 
# ----------------------------------------------

# Informations pour cliquer sur les niveaux avec la souri 
# La position des niveaux sur la carte
                  # top left  bottom right
posButtonLevel1 = [(16, 358), (260, 438)]  # positions de la chaussure Niveau1 = (140, 400)
posButtonLevel2 = [(209, 188), (451, 269)]
posButtonLevel3 = [(388, 569), (630, 650)]
posButtonLevel4 = [(516, 314), (763, 394)]
posButtonLevel5 = [(788, 171), (1031, 249)]
            # level1    level2      level3
posShoe = [(140, 400), (330, 782), (512.29, 612.485)]
# Tableau des positions de la souris
tabLevelsPos = [posButtonLevel1, posButtonLevel2, posButtonLevel3, posButtonLevel4, posButtonLevel5]

# Classe pour les faire si oui ou non les niveau son debloques 
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        if status == 'available':  # Si le niveau est debloque
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)
        
    def update(self):
        if self.status == 'available':
            self.image = self.image 
        else:
            tint_surf = self.image.copy()  # On change la teinte de la surface si le niveau n'est pas debloque
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))
            
# Class pour faire l'icone de la chaussure 
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        # Curseur du joueur sur la carte
        self.image = pygame.image.load('../../design/overworld/shoe.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        self.rect.center = self.pos 

# Class pour creer l'overworld 
class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, fini):
        # Setup 
        self.display_surface = surface 
        if fini == True :  # Si le joueur fini le jeu alors il a acces a tous les nieaux
            self.max_level = 5
        else : 
            self.max_level = max_level
        self.current_level = start_level 
        self.create_level = create_level 
        
        # Mouvement logic
        self.moving = False  # Il ne bouge pas au depart
        # On utilise des vecteurs pour faire se deplacer l'icone de la chaussure
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8  # La vitesse de l'icone
        
        # Mise en place des noeuds et de l'icone  
        self.setup_nodes()
        self.setup_icon()
        
        # Fond
        self.the_fond = pygame.image.load('../../design/overworld/map.png').convert_alpha()
        
        # Time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False 
        self.timer_length = 500

    # Fond 
    def draw_back(self, surface):
        self.fond = surface.blit(self.the_fond, (0, 0))

    # Les noeuds
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        
        for index, node_data in enumerate(levels.values()):
            if index != 5:
                if index+1 <= self.max_level:  # Si le niveau est debloque
                    node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
                else:
                    node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])         
                self.nodes.add(node_sprite)

    # Dessine les liens entre les niveaux debloques 
    def draw_paths(self):
        if self.max_level > 1:
             points = [node['node_pos'] for index, node in enumerate(levels.values()) if index+1 <= self.max_level]
             pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)  # La ligne
       
    # Mise en place de l'icone 
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level-1].rect.center)
        self.icon.add(icon_sprite)

    # Interactions avec les touches du clavier 
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:  # Si la chaussure ne bouge pas
            posMouse = pygame.mouse.get_pos()
            if self.current_level < self.max_level and keys[pygame.K_RIGHT]:  # La chaussure bouge vers la droite
                self.move_direction = self.get_mouvement_data('next')
                self.current_level += 1
                self.moving = True 
            elif keys[pygame.K_LEFT] and self.current_level > 1:  # La chaussure bouge vers la gauche
                self.move_direction = self.get_mouvement_data('previous')
                self.current_level -= 1
                self.moving = True 
            elif keys[pygame.K_RETURN]:  # On clique sur le niveau
                self.create_level(self.current_level)
            # Si on clique avec le souris pour choisir le niveau
            elif pygame.mouse.get_pressed()[0]:
                for i in range(self.max_level):
                    if (tabLevelsPos[i][0][0] <= posMouse[0] <= tabLevelsPos[i][1][0] and
                    tabLevelsPos[i][0][1] <= posMouse[1] <= tabLevelsPos[i][1][1]) and pygame.mouse.get_pressed():
                        self.moving = True
                        self.create_level(i+1)

    # Fait en sorte que la chaussure bouge d'un niveau a l'autre en suivant un vecteur 
    def get_mouvement_data(self, target):
        # On fait -1 parce qu'on prend que des indices (c'est donc l'indice du niveau courant)
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        if target == 'next':
            # Pas d'indice parce que c'est l'indice du niveau n+1
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        else:
            # Indice -2 car c'est l'indice du niveau n-1
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 2].rect.center)
        return (end-start).normalize()

    # Fait en sorte que la chaussure avance d'un niveau a l'autre et va au centre du niveau 
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed  # Ajoute la vitesse a l'icone
            target_node = self.nodes.sprites()[self.current_level - 1]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)  # Bouge selon le vecteur (0,0)

    # Met en place un timer pour que l'animation de la chaussure ne soit pas trop rapide 
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True
    
    # Tout ce qui va etre recalculer pendant le jeu
    def run(self):
        self.input_timer()
        self.draw_back(self.display_surface)
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.nodes.update()


# -*- coding: utf-8 -*-
"""
overworld 
"""

import pygame
from game_data import levels 
from support import import_folder

                  # top left  bottom right
posButtonLevel1 = [(16, 358), (260, 438)] # pos shoe level1 = (140, 400)
posButtonLevel2 = [(209, 188), (451, 269)]
posButtonLevel3 = [(388, 569), (630, 650)]
            # level1    level2      level3
posShoe = [(140, 400), (330, 782), (512.29, 612.485)]


tabLevelsPos = [posButtonLevel1, posButtonLevel2, posButtonLevel3]
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        if status == 'available':
            self.status = 'available'
            self.tableLevel = [posButtonLevel1]
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)
        
    def update(self):
        if self.status == 'available':
            self.image = self.image 
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf,(0,0))
            

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos 
        self.image = pygame.image.load('../../design/overworld/shoe.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
    def update(self):
        self.rect.center = self.pos 
        
class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        # setup 
        self.display_surface = surface 
        self.max_level = 3#max_level
        self.current_level = start_level 
        self.create_level = create_level 
        
        # mouvement logic
        self.moving = False 
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        
        # sprites 
        self.setup_nodes()
        self.setup_icon()
        
        #fond
        self.the_fond = pygame.image.load('../../design/overworld/map.png').convert_alpha()
        
        #time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False 
        self.timer_length = 500
        
    def draw_back(self,surface):
        self.fond = surface.blit(self.the_fond,(0,0))

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        
        for index, node_data in enumerate(levels.values()):
            if index+1 <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed,node_data['node_graphics'])         
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])         
            self.nodes.add(node_sprite)
                   
    def draw_paths(self):
        if self.max_level >1:
             points = [node['node_pos'] for index,node in enumerate(levels.values()) if index+1 <= self.max_level]
             pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)
             #print(self.icon.sprite.pos)
       
           
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level-1].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            posMouse = pygame.mouse.get_pos()
            if self.current_level < self.max_level and keys[pygame.K_RIGHT] :
                self.move_direction = self.get_mouvement_data('next')
                self.current_level += 1
                self.moving = True 
            elif keys[pygame.K_LEFT] and self.current_level > 1:
                self.move_direction = self.get_mouvement_data('previous')
                self.current_level -= 1
                self.moving = True 
            elif keys[pygame.K_RETURN]:
                self.create_level(self.current_level)
            # si on clique avec le souris pour choisir le niveau
            elif pygame.mouse.get_pressed()[0]:
                for i in range(self.max_level):
                    if (tabLevelsPos[i][0][0] <= posMouse[0] <= tabLevelsPos[i][1][0] and
                    tabLevelsPos[i][0][1] <= posMouse[1] <= tabLevelsPos[i][1][1]) and pygame.mouse.get_pressed():
                        self.moving = True
                        self.create_level(i+1)



    def get_mouvement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level -1].rect.center) #on fait des -1 parce qu'on prend que des indices (c'est donc l'indice du niveau courant) 
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center) #pas d'indice parce que c'est l'indice du niveau n+1
        else: 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level -2].rect.center)  #indice -2 car c'est l'indice du niveau n-1
        return (end-start).normalize()
        
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed 
            target_node = self.nodes.sprites()[self.current_level -1]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
        
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True
        
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
        """
        posMouse = pygame.mouse.get_pos()
        print(posMouse)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(posMouse)
        """
        
        
        
        
        
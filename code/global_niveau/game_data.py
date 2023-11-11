# -*- coding: utf-8 -*-
"""
clear code le platformer complet, partie 2 sur le visual level editor, game_data
"""
#attention, a changer suivant les niveaux 
level_1 = {'terrain': '../../design/niveau1/map/level_1_map_terrain.csv',
           'item': '../../design/niveau1/map/level_1_map_items.csv',
           'enemies': '../../design/niveau1/map/level_1_map_enemies.csv',
           'constraints': '../../design/niveau1/map/level_1_map_constraints.csv',
           'player':'../../design/niveau1/map/level_1_map_player.csv',
           'node_pos': (140,400),
           'unlock': 2,
           'node_graphics': '../../design/overworld/1.png',
           'animation_speed': 0.15,
           'status': 'stand',
           'speed': 8,
           'gravity': 0.8,
           'jump_speed': -16,
           'items' : ['arc', 'lyre', 'montre']
           } #design/

level_2 = {'terrain': '../../design/niveau1/map/level_1_map_terrain.csv',
           'item': '../../design/niveau1/map/level_1_map_items.csv',
           'enemies': '../../design/niveau1/map/level_1_map_enemies.csv',
           'constraints': '../../design/niveau1/map/level_1_map_constraints.csv',
           'player':'../../design/niveau1/map/level_1_map_player.csv',
           'node_pos': (330,230),
           'unlock': 3,
           'node_graphics': '../../design/overworld/2.png',
           'animation_speed': 0.05,
           'status': 'swim',
           'speed': 1,
           'gravity': 0.01,
           'jump_speed': -1,
           'items' : ['fourchette', 'peanut butter', 'trident']
           }

level_3 = {'terrain': '../../design/niveau1/map/level_1_map_terrain.csv',
           'item': '../../design/niveau1/map/level_1_map_items.csv',
           'enemies': '../../design/niveau1/map/level_1_map_enemies.csv',
           'constraints': '../../design/niveau1/map/level_1_map_constraints.csv',
           'player':'../../design/niveau1/map/level_1_map_player.csv',
           'node_pos': (510,610),
           'unlock': 4,
           'node_graphics': '../../design/overworld/3.png',
           'animation_speed': 0.15,
           'status': 'stand',
           'speed': 8,
           'gravity': 0.8,
           'jump_speed': -16,
           'items' : ['livre', 'casque', 'potion']
           }
 
level_4 = {'terrain': '../../design/niveau1/map/level_1_map_terrain.csv',
           'item': '../../design/niveau1/map/level_1_map_items.csv',
           'enemies': '../../design/niveau1/map/level_1_map_enemies.csv',
           'constraints': '../../design/niveau1/map/level_1_map_constraints.csv',
           'player':'../../design/niveau1/map/level_1_map_player.csv',
           'node_pos': (640,350),
           'unlock': 5,
           'node_graphics': '../../design/overworld/4.png',
           'animation_speed': 0.15,
           'status': 'stand',
           'speed': 8,
           'gravity': 0.8,
           'jump_speed': -16,
           'items' : ['ciseaux', 'amour', 'pelle']
           }

level_5 = {'terrain': '../../design/niveau1/map/level_1_map_terrain.csv',
           'item': '../../design/niveau1/map/level_1_map_items.csv',
           'enemies': '../../design/niveau1/map/level_1_map_enemies.csv',
           'constraints': '../../design/niveau1/map/level_1_map_constraints.csv',
           'player':'../../design/niveau1/map/level_1_map_player.csv',
           'node_pos': (910,210),
           'unlock': 5,
           'node_graphics': '../../design/overworld/5.png',
           'animation_speed': 0.15,
           'status': 'stand',
           'speed': 8,
           'gravity': 0.8,
           'jump_speed': -16,
            'items' : [None, None, None] #y'a pas d'item au niveau 5 enfaite
           }

levels = {
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5}

















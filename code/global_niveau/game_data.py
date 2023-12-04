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
           'items': ['arc', 'lyre', 'montre'],
           'rotation': 0,
           'monsters': ['../../design/niveau1/monster/cyclope_w', '../../design/niveau1/monster/satyr', '../../design/niveau1/monster/cow_1', '../../design/niveau1/monster/cow_2']
           } #design/

level_2 = {'terrain': '../../design/niveau2/map/level_2_map_terrain.csv',
           'item': '../../design/niveau2/map/level_2_map_items.csv',
           'enemies': '../../design/niveau2/map/level_2_map_enemies.csv',
           'constraints': '../../design/niveau2/map/level_2_map_constraints.csv',
           'player':'../../design/niveau2/map/level_2_map_player.csv',
           'node_pos': (330,230),
           'unlock': 3,
           'node_graphics': '../../design/overworld/2.png',
           'animation_speed': 0.05,
           'status': 'swim',
           'speed': 4,
           'gravity': 0.04,
           'jump_speed': -2,
           'items': ['fourchette', 'peanut butter', 'trident'],
           'rotation': -90,
           'monsters': ['../../design/niveau2/monster/fish', '../../design/niveau2/monster/mermaid', '../../design/niveau2/monster/poulpe']
           }

level_3 = {'terrain': '../../design/niveau3/map/level_3_map_terrain.csv',
           'item': '../../design/niveau3/map/level_3_map_items.csv',
           'enemies': '../../design/niveau3/map/level_3_map_enemies.csv',
           'constraints': '../../design/niveau3/map/level_3_map_constraints.csv',
           'player':'../../design/niveau3/map/level_3_map_player.csv',
           'node_pos': (510,610),
           'unlock': 4,
           'node_graphics': '../../design/overworld/3.png',
           'animation_speed': 0.15,
           'status': 'stand',
           'speed': 8,
           'gravity': -0.8,
           'jump_speed': -16,
           'items': ['livre', 'casque', 'potion'],
           'rotation': -180,
           'monsters': ['../../design/niveau3/monster/cerber', '../../design/niveau3/monster/ghost', '../../design/niveau3/monster/skeleton']
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
           'items' : ['ciseaux', 'amour', 'pelle'],
           'rotation':0,
           'monsters': ['../../design/niveau4/monster/bat', '../../design/niveau4/monster/fire', '../../design/niveau4/monster/stalactite']
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
            'items' : [None, None, None], #y'a pas d'item au niveau 5 enfaite,
            'rotation':0,
            'monsters': ['../../design/niveau1/monster/cyclope_w', '../../design/niveau1/monster/satyr', '../../design/niveau1/monster/cow_1', '../../design/niveau1/monster/cow_2']
           }

levels = {
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5}















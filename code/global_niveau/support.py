# -*- coding: utf-8 -*-
"""
support
"""

# ---------------- IMPORTATIONS ----------------
import pygame
from csv import reader 
from settings import tile_size 
from os import walk
# ----------------------------------------------

# Permet d'importer des dossiers 
def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:  # On a le nom de chaque image qu'il y a dans le dossier du path
            full_path = path + '/' + image 
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list 

# Permet d'importer des fichiers CSV
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map 

# Permet d'importer des images qu'on va ensuite recouper pour correspondre aux tiles du niveau 
def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size) 
    tile_num_y = int(surface.get_size()[1] / tile_size)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size 
            y = row * tile_size 
            new_surf = pygame.Surface((tile_size,tile_size))
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    print(cut_tiles)
    return cut_tiles 



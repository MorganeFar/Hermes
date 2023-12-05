# -*- coding: utf-8 -*-
"""
main
"""
import pygame, sys
from settings import screen_height, screen_width
from level import Level
from overworld import Overworld 
from ui import UI
import gameOver
from dialogues import Dialogue
#from gameOver import over

class Game:
    def __init__(self):
        # game attributes
        self.max_level = 1
        self.max_health = 3
        self.cur_health = 3
        self.item = None  # a voir si on fait comme ca pour les items
        
        # audio
        self.level_bg_music = ['', pygame.mixer.Sound('../../audio/ambiance_niv1.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv2.wav'), pygame.mixer.Sound('../../audio/ambiance_niv3.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv4.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv5.mp3')]
        self.overworld_bg_music = pygame.mixer.Sound('../../audio/overworld.mp3')
        self.dead_sound = pygame.mixer.Sound('../../audio/dead.wav')
        
        # overworld creation
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        self.status = 'overworld' # le status de ou se trouve le joueur
        self.overworld_bg_music.play(loops=-1)
        
        # user interface
        self.ui = UI(screen)

        #dialogues variables 
        self.recom_niveaux = [False, False, False, False, False]
        
    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_item, self.change_health, self.create_dialogue)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.bg_music = self.level_bg_music[current_level]
        self.bg_music.play(loops=-1)
        self.item = None
        # self.cur_health = 3 #normalement dès qu'il relance le niveau, donc des que game over
        
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
            self.cur_health = 3 
        else:
            self.dead_sound.play()
            gameOver.over()
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.bg_music.stop()
        self.overworld_bg_music.play(loops=-1)

    def create_dialogue(self, current_level):
        self.dialogue = Dialogue(current_level, self.item, self.recom_niveaux[current_level -1])
        self.dialogue.run()
        self.recom_niveaux[current_level -1] = True
    
    def change_item(self, lequel):
        self.item = lequel 
        
    def change_health(self, amount):
        self.cur_health += amount 
        
    def check_game_over(self):
        if self.cur_health <= 0:
            self.dead_sound.play()
            self.cur_health = 3 
            self.item = None 
            self.max_level = 1
            gameOver.over()
            self.overworld = Overworld(1, self.max_level, screen, self.create_level)
            self.bg_music.stop()
            self.overworld_bg_music.play(loops=-1)
            self.status = 'overworld'
            
    def run(self):
        if self.status == 'overworld': # switch entre les différents niveaux et la 'map' (l'overworld)
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health)
            self.ui.show_item(self.item)
            self.check_game_over()
            
#setup 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()

    pygame.display.update()
    clock.tick(60)
"""
def start():
    while not game.level.isDead : # check si le perso est vivant
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        game.run()
  
        pygame.display.update()
        clock.tick(60)
    return game.level.isDead

start()
"""

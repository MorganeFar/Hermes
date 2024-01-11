# -*- coding: utf-8 -*-
"""
main
"""

# ---------------- IMPORTATIONS ----------------
import pygame, sys
from settings import screen_height, screen_width
from level import Level
from overworld import Overworld 
from ui import UI
import gameOver
from dialogues import Dialogue
import welcome
sys.path.append('../') 
import maia_dialogue
# -----------------------------------------------


# ---------------- CLASSE DU JEU ----------------
class Game:
    def __init__(self):
        # Attributs du jeu
        self.max_level = 1      # Niveau maximum atteind par le joueur (au debut il n'y a que le 1)
        self.max_health = 3     # Nombre de vies (coeurs) maximum autorise
        self.cur_health = 3     # Le joueur ne s'est pas encore fait touche donc il a le max de vies
        self.item = None        # Aucun objet recuperer au debut
        self.cur_levl = 1       # niveau actuel => a l'initialisation c'est le 1
        
        # Audio
        self.level_bg_music = ['', pygame.mixer.Sound('../../audio/ambiance_niv1.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv2.wav'), pygame.mixer.Sound('../../audio/ambiance_niv3.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv4.mp3'), pygame.mixer.Sound('../../audio/ambiance_niv5.mp3')]
        self.overworld_bg_music = pygame.mixer.Sound('../../audio/overworld.mp3')
        self.dead_sound = pygame.mixer.Sound('../../audio/dead.wav')
        self.welcome_sound = pygame.mixer.Sound('../../audio/welcome.mp3')
        self.dialogue_sound = pygame.mixer.Sound('../../audio/dialogue.mp3')
        self.gameOver_sound = pygame.mixer.Sound('../../audio/gameover.ogg')
        
        # Accueil du joueur et commencement du jeu
        self.welcome_sound.play(loops=-1)
        welcome.welcomeMenu()       # Lancement page d'accueil JOUER
        self.welcome_sound.stop()
        self.dialogue_sound.play(loops=-1)
        maia_dialogue.run()         # Lancement du premier dialogue
        self.dialogue_sound.stop()
        self.fini = True#False           # Etat du jeu : en cours ou fini
        # Creation de la carte (overworld)
        self.overworld = Overworld(1, self.max_level, screen, self.create_level, self.fini)
        self.status = 'overworld'  # Status d'ou se trouve le joueur
        self.overworld_bg_music.play(loops=-1)
        
        # Interface utilisateur
        self.ui = UI(screen, self.cur_levl)

        # Variables des dialogues
        self.recom_niveaux = [False, False, False, False, False, False]

    # Creation du niveau sur lequel le joueur se trouve
    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_item, self.change_health, self.create_dialogue)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.bg_music = self.level_bg_music[current_level]
        self.bg_music.play(loops=-1)
        self.item = None
        self.cur_levl = current_level 
        self.ui = UI(screen, self.cur_levl)
        # Si le joueur a reussi le dernier niveau
        if current_level == 5:
            self.fini = True 

    # Mise a jour de la carte en fonction de l'evolution du joueur
    def create_overworld(self, current_level, new_max_level, final):
        self.bg_music.stop()
        self.dialogue_sound.stop()
        if final == 'gagne':        # Le joueur a reussi le niveau
            self.cur_health = 3     # Remise a 0 du compteur de vie pour le niveau suivant
            if new_max_level > self.max_level:
                self.max_level = new_max_level  # Mise a jour niveau max
                if self.fini:
                    self.max_level = 5
        else:                       # Le joueur n'a pas reussi le niveau
            self.dead_sound.play()
            self.gameOver_sound.play(loops=-1)
            gameOver.over()         # Affichage de la page du game over
            self.gameOver_sound.stop()
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self.fini)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

    # Affichage des dialogues en fonction du niveau et de la reussite du joueur
    def create_dialogue(self, current_level):
        if current_level != 5:
            self.bg_music.stop()
            self.dialogue_sound.play(loops=-1)
        self.dialogue = Dialogue(current_level, self.item, self.recom_niveaux[current_level -1])
        self.dialogue.run()
        self.recom_niveaux[current_level -1] = True

    # Collecte des objets
    def change_item(self, lequel):
        self.item = lequel 

    # Changement du niveau de vie 
    def change_health(self, amount):
        self.cur_health += amount 

    # Verification de l'etat du joueur, ici s'il est mort
    def check_game_over(self):
        if self.cur_health <= 0:    # le joueur a perdu ses 3 vies
            self.dead_sound.play()
            # Remise a 0 des attributs
            self.cur_health = 3 
            self.item = None 
            self.max_level = 1
            self.bg_music.stop()
            self.gameOver_sound.play(loops=-1)
            gameOver.over()     # Affichage de la page de game over
            self.gameOver_sound.stop()
            # Affichage de l'overworld
            self.overworld = Overworld(1, self.max_level, screen, self.create_level, self.fini)
            self.overworld_bg_music.play(loops=-1)
            self.status = 'overworld'

    # Methode coordonnant les methodes pour jouer
    def run(self):
        if self.status == 'overworld':  # Switch entre les différents niveaux et la carte (l'overworld)
            self.overworld.run()
        else:
            self.level.run()    # Lancement du niveau
            self.ui.show_health(self.cur_health)  # Affichage de l'etat de 'sante' du joueur
            if self.cur_levl != 5:
                self.ui.show_item(self.item)    # Affichage de la collecte d'objet
            self.check_game_over()              # Verification de si le joueur est mort

# ------------------------------------------------

# -------------------- SETUP --------------------
pygame.init()
# Creation d'une fenetre pygame
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()  # Creation du jeu

while True:
    for event in pygame.event.get():
        # Ferme la fernetre et stoppe le script si le joueur clique sur la croix
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()  # Lancement du jeu

    pygame.display.update()  # Mise a jour du visuel
    clock.tick(60)           # Temps entre chaque rafraichissements

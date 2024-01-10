# -*- coding: utf-8 -*-
"""
les dialogues 
"""

# ---------------- IMPORTATIONS ----------------
import pygame, sys
from sceneryClass import Scenery
from game_data import levels
from settings import screen_height, screen_width 
# ----------------------------------------------

class Dialogue:
    def __init__(self, current_level, objet, recommence): # Current_level est le level courrant (int), objet est l'objet courant (str), et recommenceest une condition si on recommence ou pas (booleen)
        # Global 
        self.current_level = current_level
        self.recommence = recommence 
        self.level_data = levels[self.current_level] # Pour avoir acces au data du niveau 
        
        # Window
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        if current_level != 6 :
            path = "../../design/niveau" + str(self.current_level) + "/background.png"
        else : 
            path = "../../design/the_end/olympe.png"
        self.background = pygame.image.load(path)
        self.fond = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.fond = self.fond.convert()
        
        # Les objets 
        self.objet = objet 
        self.bon_obj = self.level_data['bon_obj'] # Le bon objet est l'objet que doit recuperer le joueur pour continuer 
        self.mauv_obj1 = self.level_data['mauv_obj1']
        self.mauv_obj2 = self.level_data['mauv_obj2']

        # Booleens qui permettent de savoir quel objet le joueur a ramasse
        self.objet_bon = False
        self.objet_mauv1 = False
        self.objet_mauv2 = False
        
        if self.objet == self.bon_obj :
            self.objet_bon = True
        elif self.objet == self.mauv_obj1:
            self.objet_mauv1 = True
        elif self.objet == self.mauv_obj2:
            self.objet_mauv2 = True
        
        # Color
        self.light_grey = (200, 200, 200)
        self.black = (0,0,0)
        self.yellow = (230, 219, 65)
        
        # Mise en place de la scene avec le dieu et Hermes 
        self.place = self.level_data['place_dieu']
        self.olympeGroup = pygame.sprite.Group()
        if self.current_level != 5:
            self.dieu = Scenery(self.place[0], self.place[1], self.place[2], self.place[3], self.level_data['dieu'])
            self.olympeGroup.add(self.dieu)
        
        hermes = Scenery(0.2, 0.40, 0.10, 0.3, ["../../design/hermes/stand/hermes_s.png"])
        self.olympeGroup.add(hermes)

        # Contenu des dialogues 
        self.dialogue_all = self.level_data['dialogue_all']
        self.dialogue_bon_obj = self.level_data['dialogue_bon_obj']
        self.dialogue_mauv_obj1 = self.level_data['dialogue_mauv_obj1']
        self.dialogue_mauv_obj2 = self.level_data['dialogue_mauv_obj2']
        self.dialogue_no = self.level_data['dialogue_no']
        self.dialogue_recom = self.level_data['dialogue_recom']

        # Variables pour le texte 
        self.game_font = pygame.font.Font("freesansbold.ttf", 25) # Le font et la taille du texte 
        self.zone_text = pygame.Rect(0, screen_height-(screen_height/4), screen_width , screen_height/4) # La zone dans laquelle il y aura le texte
        # Les boutons d'indication des touches pour le joueur 
        self.bouton_suivant = pygame.Rect(screen_width-90, screen_height-50, 70, 30)
        self.bouton_sortir = pygame.Rect(screen_width-180, screen_height-50, 80, 30)

        self.counter = 0 # Aide a savoir si on est a la fin du message 
        self.speed = 2 # On a 1 caract tous les 2 tics 
        self.active_message = 0 # L'indice du message 
        self.active_mess_objets = -1
        self.done = False # Indique si le message est fini    

        if not self.recommence: # Le message du debut differe si il recommence le niveau ou non 
            self.message = self.dialogue_all[self.active_message] #le message actuel
        else:
            self.message = self.dialogue_recom[0]

        #score timer 
        self.score_time = True

    # Met en place des objets speciaux dans le dialogue du niveau 4
    def objets(self):
        self.trone = Scenery(0.3, 0.4, 0.16, 0.32, ["../../design/niveau4/obj_spe/trone.png"])
        self.olympeGroup.add(self.trone)
        self.shoes = Scenery(0.45, 0.61, 0.12, 0.1, ["../../design/niveau4/obj_spe/chaussure.png"])
        self.olympeGroup.add(self.shoes)

    # Met en place le trone pour le dialogue de fin avec Zeus 
    def chaise(self):
        self.chair = Scenery(0.3, 0.4, 0.16, 0.32, ["../../design/niveau4/obj_spe/trone.png"])
        self.olympeGroup.add(self.chair)

    # Met en place hera dans le dialogue du niveau 5 
    def hera(self):
        self.dieu = Scenery(self.place[0], self.place[1], self.place[2], self.place[3], self.level_data['dieu'])
        self.olympeGroup.add(self.dieu)

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        
        while True:

            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed * len(self.message):
                self.done = True 
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                
                # Si on presse entrer on passe au texte suivant 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.done and not self.recommence and self.active_message < len(self.dialogue_all) -1: # Si le joueur en est a son premier coup 
                        self.active_message += 1
                        self.done = False 
                        self.message = self.dialogue_all[self.active_message]
                        self.counter = 0
                        if (self.active_message == 1) and (self.current_level == 6):
                            self.chaise()
                        if (self.active_message == 1) and (self.current_level == 5):
                            self.hera()
                    
                    else: # Texte suivant selon l'objet ramasse 
                        # Si le joueur a ramasse le bon objet  
                        if event.key == pygame.K_RETURN and self.done and self.objet_bon and self.active_mess_objets < len(self.dialogue_bon_obj) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_bon_obj[self.active_mess_objets]
                            self.counter = 0
                            if (self.active_mess_objets == 5) and (self.current_level == 4):
                                self.objets()
                        # Si le joueur a ramassé le mauvais obj 1
                        elif event.key == pygame.K_RETURN and self.done and self.objet_mauv1 and self.active_mess_objets < len(self.dialogue_mauv_obj1) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_mauv_obj1[self.active_mess_objets]
                            self.counter = 0
                        # Si le joueur a ramassé le mauvais obj 2
                        elif event.key == pygame.K_RETURN and self.done and self.objet_mauv2 and self.active_mess_objets < len(self.dialogue_mauv_obj2) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_mauv_obj2[self.active_mess_objets]
                            self.counter = 0
                        # Si le joueur n'a ramassé aucun objet
                        elif event.key == pygame.K_RETURN and self.done and (not self.objet_mauv1 and not self.objet_mauv2 and not self.objet_bon) and self.active_mess_objets < len(self.dialogue_no) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_no[self.active_mess_objets]
                            self.counter = 0
                        elif event.key == pygame.K_e:
                            return 'final'
                            
            # Visuel
            self.screen.blit(self.fond, (0,-(screen_height/4)))

            # Les personnages
            self.olympeGroup.draw(self.screen)
            
            # La zone de texte et les boutons
            pygame.draw.rect(self.screen, self.light_grey, self.zone_text)
            pygame.draw.rect(self.screen, self.yellow, self.bouton_suivant)
            pygame.draw.rect(self.screen, self.yellow, self.bouton_sortir)
            suivant_font = pygame.font.Font("freesansbold.ttf", 18)
            suivant = suivant_font.render("Enter", True, 'black')
            sortir = suivant_font.render("Exit: 'e'", True, 'black')
            self.screen.blit(suivant, (screen_width-80, screen_height-45))
            self.screen.blit(sortir, (screen_width-170, screen_height-45))
            
            # On cree du texte anime
            self.surface = self.screen 
            text = self.message[0:self.counter//self.speed]
            pos = (screen_width*0.02, screen_height-(screen_height/4) + screen_height*0.02)
            color = 'black'
            
            # Animation de retour a la ligne et de lettre par lettre
            collection = [word.split(' ') for word in text.splitlines()]
            space = self.game_font.size(' ')[0]
            x,y = pos 
            for lines in collection:
                for words in lines:
                    word_surface = self.game_font.render(words, True, color)
                    word_width , word_height = word_surface.get_size()
                    if x + word_width >= screen_width*0.98:
                        x = pos[0]
                        y += word_height 
                    self.surface.blit(word_surface, (x,y))
                    x += word_width + space 
                x = pos[0]
                y += word_height
                
            pygame.display.flip()
            
            clock.tick(60)


# -*- coding: utf-8 -*-
"""
les dialogues 
"""

import pygame, sys
from sceneryClass import Scenery
from game_data import levels
from settings import screen_height, screen_width 

class Dialogue:
    def __init__(self, current_level, objet, recommence): #current_level le level courrant (int), objet l'objet courant (str), et recommence condition si on recommence ou pas (booleen)
        #global 
        self.current_level = current_level
        self.recommence = recommence 
        self.level_data = levels[self.current_level]
        
        #window
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        path = "../../design/niveau" + str(self.current_level) + "/background.png"
        self.background = pygame.image.load(path)
        self.fond = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.fond = self.fond.convert()
        
        #les objets 
        self.objet = objet 
        self.bon_obj = self.level_data['bon_obj']
        self.mauv_obj1 = self.level_data['mauv_obj1']
        self.mauv_obj2 = self.level_data['mauv_obj2']
        
        self.objet_bon = False
        self.objet_mauv1 = False
        self.objet_mauv2 = False
        
        if self.objet == self.bon_obj :
            self.objet_bon = True
        elif self.objet == self.mauv_obj1:
            self.objet_mauv1 = True
        elif self.objet == self.mauv_obj2:
            self.objet_mauv2 = True
        
        #color
        self.light_grey = (200, 200, 200)
        self.black = (0,0,0)
        self.yellow = (230, 219, 65)
        
        #Scenery
        self.place = self.level_data['place_dieu']
        self.olympeGroup = pygame.sprite.Group()
        self.dieu = Scenery(self.place[0], self.place[1], self.place[2], self.place[3], self.level_data['dieu'])
        self.olympeGroup.add(self.dieu)
        
        hermes = Scenery(0.2, 0.40, 0.10, 0.3, ["../../design/hermes/stand/hermes_s.png"])
        self.olympeGroup.add(hermes)

        #contenu des dialogues 
        self.dialogue_all = self.level_data['dialogue_all']
        self.dialogue_bon_obj = self.level_data['dialogue_bon_obj']
        self.dialogue_mauv_obj1 = self.level_data['dialogue_mauv_obj1']
        self.dialogue_mauv_obj2 = self.level_data['dialogue_mauv_obj2']
        self.dialogue_no = self.level_data['dialogue_no']
        self.dialogue_recom = self.level_data['dialogue_recom']

        #text variables
        self.game_font = pygame.font.Font("freesansbold.ttf", 25) #le font et la taille du texte 
        self.zone_text = pygame.Rect(0, screen_height-(screen_height/4), screen_width , screen_height/4) #la zone dans laquelle il y aura le texte 
        self.bouton_suivant = pygame.Rect(screen_width-90, screen_height-50, 70, 30)
        self.bouton_sortir = pygame.Rect(screen_width-180, screen_height-50, 80, 30)

        self.counter = 0 #aide a savoir si on est a la fin du message 
        self.speed = 2 #on a 1 caract tous les 2 tics 
        self.active_message = 0 #l indice du message 
        self.active_mess_objets = -1
        self.done = False        

        if not self.recommence: #le message du debut differe si il recommence me niveau ou non 
            self.message = self.dialogue_all[self.active_message] #le message actuel
        else:
            self.message = self.dialogue_recom[0]

        #score timer 
        self.score_time = True

    def run(self):
        pygame.init() #always need for any kind of pygame code 
        clock = pygame.time.Clock()
        """final = 'perdu'
        if self.objet_bon == True :
            final = 'gagne'"""
        while True: #the loop 

            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed * len(self.message):
                self.done = True 
            
            for event in pygame.event.get(): #any movement or intercation or action
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                
                #si on presse entrer on passe au texte suivant 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.done and not self.recommence and self.active_message < len(self.dialogue_all) -1: #si il est a son premier coup 
                        self.active_message += 1
                        self.done = False 
                        self.message = self.dialogue_all[self.active_message]
                        self.counter = 0
                    
                    else: #texte suivant selon l'objet ramasse 
                        #si le joueur a ramassé la lyre 
                        if event.key == pygame.K_RETURN and self.done and self.objet_bon and self.active_mess_objets < len(self.dialogue_bon_obj) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_bon_obj[self.active_mess_objets]
                            self.counter = 0
                        #si le joueur a ramassé l'arc
                        elif event.key == pygame.K_RETURN and self.done and self.objet_mauv1 and self.active_mess_objets < len(self.dialogue_mauv_obj1) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            #self.dialogue_obj = cas(objet1)
                            self.message = self.dialogue_mauv_obj1[self.active_mess_objets]
                            self.counter = 0
                        #si le joueur a ramassé la montre 
                        elif event.key == pygame.K_RETURN and self.done and self.objet_mauv2 and self.active_mess_objets < len(self.dialogue_mauv_obj2) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            #self.dialogue_obj = cas(objet2)
                            self.message = self.dialogue_mauv_obj2[self.active_mess_objets]
                            self.counter = 0
                        #si le joueur n'a ramassé aucun objet
                        elif event.key == pygame.K_RETURN and self.done and (not self.objet_mauv1 and not self.objet_mauv2 and not self.objet_bon) and self.active_mess_objets < len(self.dialogue_no) -1:
                            self.active_mess_objets += 1
                            self.done = False 
                            self.message = self.dialogue_no[self.active_mess_objets]
                            self.counter = 0
                        elif event.key == pygame.K_e:
                            #status = 'overworld'
                            return 'final'
                            
            #visual 
            self.screen.blit(self.fond, (0,-(screen_height/4)))

            #les personnages
            self.olympeGroup.draw(self.screen)
            #la zone de texte et le bouton suivant
            pygame.draw.rect(self.screen, self.light_grey, self.zone_text)
            pygame.draw.rect(self.screen, self.yellow, self.bouton_suivant)
            pygame.draw.rect(self.screen, self.yellow, self.bouton_sortir)
            suivant_font = pygame.font.Font("freesansbold.ttf", 18)
            suivant = suivant_font.render("Enter", True, 'black')
            sortir = suivant_font.render("Exit: 'e'", True, 'black')
            self.screen.blit(suivant, (screen_width-80, screen_height-45))
            self.screen.blit(sortir, (screen_width-170, screen_height-45))
            
            #on cree du texte anime
            self.surface = self.screen 
            text = self.message[0:self.counter//self.speed]
            pos = (screen_width*0.02, screen_height-(screen_height/4) + screen_height*0.02)
            color = 'black'
            
            #animation de retour a la ligne et de lettre par lettre
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
            
            #updating the window 
            pygame.display.flip()
            
            clock.tick(60)

    

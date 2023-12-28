# -*- coding: utf-8 -*-
"""
la cinematique de debut avec maia
"""

import pygame, sys
sys.path.append('global_niveau') 
from sceneryClass import Scenery


def run():

    dialogue_all = ["Maïa – Bonjour mon fils.",
                    "Maïa – J'ai pris connaissance de tes projets de conquête d'une place à l'Olympe. Félicitation pour ton courage !" ,
                    "Maïa – Pour mener à bien ta quête n’oublie pas une chose: tu peux réunir les ingrédients pour constituer le trône en faisant des échanges équivalents avec les dieux.",
                    "Maïa – Et un dernier conseil, le solstice d'été approche, Apollon, le dieu de la musique organise un grand concert.",
                    "Maïa – Il y jouera même un solo de cet instrument si mélodieux...",
                    "Maïa – Si tu l'aides pour son concert, il t'aidera en retour.",
                    "Maïa – Au revoir Hermès, et que le sort te soit favorable.", 
                    "*L'aventure peut commencer !* *appuyez sur 'e' pour sortir*"]
            
    #general setup
    pygame.init() #always need for any kind of pygame code 
    clock = pygame.time.Clock()
    
    #setting up the main window 
    screen_width = 1080
    screen_height = 704 #960
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.image.load("../../design/tuto/decor_tuto.png")
    fond = pygame.transform.scale(background, (screen_width, screen_height))
    fond = fond.convert()
    light_grey = (200, 200, 200)
    black = (0,0,0)
    yellow = (230, 219, 65)
    pygame.display.set_caption('hermes') #the title of the window 
    
    #Scenery
    olympeGroup = pygame.sprite.Group()
    maia = Scenery(0.6, 0.2, 0.1, 0.50, ["../../design/tuto/maia.png"])
    olympeGroup.add(maia)
    
    hermes = Scenery(0.3, 0.40, 0.10, 0.3, ["../../design/hermes/stand/hermes_s.png"])
    olympeGroup.add(hermes)
    
    
    #text variables
    game_font = pygame.font.Font("freesansbold.ttf", 25) #le font et la taille du texte 
    zone_text = pygame.Rect(0, screen_height-(screen_height/4), screen_width , screen_height/4) #la zone dans laquelle il y aura le texte 
    bouton_suivant = pygame.Rect(screen_width-90, screen_height-50, 70, 30)
    bouton_sortir = pygame.Rect(screen_width-180, screen_height-50, 80, 30)
    
    counter = 0 #aide a savoir si on st a la fin du message 
    speed = 2 #on a 1 caract tous les 2 tics 
    active_message = 0 #l indice du message 
    message = dialogue_all[active_message] #le message actuel 
    done = False
    
    
    #score timer 
    score_time = True
    
    while True: #the loop 
        #handling input 
        
        if counter < speed * len(message):
            counter += 1
        elif counter >= speed * len(message):
            done = True 
        
        for event in pygame.event.get(): #any movement or intercation or action
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
                #a voir dans un truc qui s appelle all pygame locals
            
            #si on presse entrer on passe au texte suivant 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done and active_message < len(dialogue_all) -1: #si on arrive au dernier message 
                    active_message += 1
                    done = False 
                    message = dialogue_all[active_message]
                    counter = 0
                elif event.key == pygame.K_e:
                    return 'final'
            
        #visual 
        screen.blit(fond, (0,-(screen_height/4)))
    
        #les personnages
        olympeGroup.draw(screen)
        #la zone de texte et le bouton suivant
        pygame.draw.rect(screen, light_grey, zone_text)
        pygame.draw.rect(screen, yellow, bouton_suivant)
        pygame.draw.rect(screen, yellow, bouton_sortir)
        suivant_font = pygame.font.Font("freesansbold.ttf", 18)
        suivant = suivant_font.render("Enter", True, 'black')
        sortir = suivant_font.render("Exit: 'e'", True, 'black')
        screen.blit(suivant, (screen_width-80, screen_height-45))
        screen.blit(sortir, (screen_width-170, screen_height-45))
        
        #on cree du texte anime
        surface = screen 
        text = message[0:counter//speed]
        pos = (screen_width*0.02, screen_height-(screen_height/4) + screen_height*0.02)
        color = 'black'
        
        #animation de retour a la ligne et de lettre par lettre 
        collection = [word.split(' ') for word in text.splitlines()]
        space = game_font.size(' ')[0]
        x,y = pos 
        for lines in collection:
            for words in lines:
                word_surface = game_font.render(words, True, color)
                word_width , word_height = word_surface.get_size()
                if x + word_width >= screen_width*0.98:
                    x = pos[0]
                    y += word_height 
                surface.blit(word_surface, (x,y))
                x += word_width + space 
            x = pos[0]
            y += word_height
        
        #updating the window 
        pygame.display.flip()
        
        clock.tick(60)
    
    

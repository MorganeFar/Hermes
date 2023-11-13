# -*- coding: utf-8 -*-
"""
la cinematique de fin avec zeus
"""

import pygame, sys
sys.path.append('global_niveau') 
from sceneryClass import Scenery

dialogue_all = ["Zeus – Hermès ! Que fais-tu ici mon fils ? Quelqu'un t'envoie me porter un message ?",
                "Hermès – Non pas aujourd'hui. Je viens placer mon trône, celui du douzième dieu de l'Olympe.", 
                "Zeus – Ton trône ? Le douzième dieu de l'Olympe ? Hahahaha ! Quel audace ! Et qu'est-ce qu'il te fait croire que je vais accepter ta requête ?",
                "Hermès – En tant que messagers des dieux, je peux aller partout où je veux et j'ai des oreilles partout donc je peux t'aider à éviter les rébellions. Je te propose donc mes services contre une place à l'Olympe.",
                "Zeus – Hmmm... Cela peut être vraiment avantageux. Et qu'est-ce qui me dit que ce n'est pas encore une ruse ?", 
                "Hermès – Je te promets de ne plus te mentir. Je ne te dirais que et uniquement la vérité.", 
                "Zeus – Ça c'est vraiment intéressant. Mais comment connais-tu la liste des ingrédients ? Je la garde toujours sur moi … *regarde dans sa poche* Elle n'est plus là ! Est-ce toi qui me l'a volé ?!", 
                "Hermès – Euuuh … peut-être.", 
                "Zeus – Ha ha ha, quel audace ! Tu es bien mon fils toi ! C'est d'accord alors. Hermès, je te proclame à partir d'aujourd'hui douzième dieu de l'Olympe !"]  
        
#general setup
pygame.init() #always need for any kind of pygame code 
clock = pygame.time.Clock()

#setting up the main window 
screen_width = 1080
screen_height = 704 #960
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../design/the_end/olympe.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()
light_grey = (200, 200, 200)
black = (0,0,0)
yellow = (230, 219, 65)
pygame.display.set_caption('zeus') #the title of the window 

#Scenery
olympeGroup = pygame.sprite.Group()
zeus = Scenery(0.6, 0.1, 0.3, 0.6, ["../design/the_end/zeus.png"])
olympeGroup.add(zeus)

hermes = Scenery(0.2, 0.40, 0.10, 0.3, ["../design/hermes/stand/hermes_s.png"])
olympeGroup.add(hermes)

def chaise():
    chair = Scenery(0.3, 0.4, 0.16, 0.32, ["../design/niveau4/object/trone.png"])
    olympeGroup.add(chair)


#text variables
game_font = pygame.font.Font("freesansbold.ttf", 25) #le font et la taille du texte 
zone_text = pygame.Rect(0, screen_height-(screen_height/4), screen_width , screen_height/4) #la zone dans laquelle il y aura le texte 
bouton_suivant = pygame.Rect(screen_width-90, screen_height-50, 70, 30)

counter = 0 #ade a savoir si on st a la fin du message 
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
                #on ajoute la chaise a partir d un certain dialogue 
                if active_message == 1:
                    chaise()
        
    #visual 
    screen.blit(fond, (0,-(screen_height/4)))

    #les personnages
    olympeGroup.draw(screen)
    #la zone de texte et le bouton suivant
    pygame.draw.rect(screen, light_grey, zone_text)
    pygame.draw.rect(screen, yellow, bouton_suivant)
    suivant_font = pygame.font.Font("freesansbold.ttf", 18)
    suivant = suivant_font.render("Enter", True, 'black')
    screen.blit(suivant, (screen_width-80, screen_height-45))
    
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


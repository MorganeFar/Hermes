# -*- coding: utf-8 -*-
"""
la cinematique de niveau 2 avec poseidon 
"""

import pygame, sys
sys.path.append('../global_niveau')
from sceneryClass import Scenery

#les dialogues
dialogue_all = ["Poséidon – Hermès ? Tu es encore là ? Je croyais qu'ils t'avaient enfin remplacé par les mails.",
                "Hermes – *pas content* Je suis venu te demander des pierres précieuses.",
                "Poséidon – Des pierres précieuses ? Pourquoi en voudrais-tu ? Si c'est Hécate qui t'envoie, dit lui que je lui en ai donné bien assez et qu'elle ne vienne plus m'ennuyer avec ça.",
                "Hermes – Personne ne m'envoie, les pierres sont pour moi. Je veux construire un trône, pour devenir le douzième dieu de l'Olympe.",
                "Poséidon – Hahaha !! Tu es bien ambitieux mon neveux. Et qu'est-ce qu'il te fait croire que je vais te donner mes précieuses pierres ?"]

#les dialogue suivant l'objet, change suivant l'objet qu'hermes a avec lui 
#l'objet utile ui fait passer au niveau suivant 
dialogue_lyre = ["Hermes – J'ai trouvé ton trident sur le chemin jusqu'ici. Je te propose dde l'échanger contre les pierres.",
                 "Poséidon – Mon trident ! Tu as de la chance dieu de la ruse. Marché conclu, voilà les pierres.",
                "Poséidon – Un conseil pour ta quête, ne traine pas trop sous terre. Le dieu des morts ne peut plus cacher sa tête d'enterrement et il a l'air contrarié.",
                "*victoire, niveau suivant*"]

#les autres objets 'inutiles' qui font recommencer le niveau 
#attention bien mettre le determinant devant le nom !!
objet1 = "une fourchette"  
objet2 = "du beurre de cacahuète"

def cas(objet): #meme texte suivant l'objet 'inutile'
    dialogue_objet = ["Hermes – J'ai " + objet + ".", 
                       "Poséidon – Sérieusement ? Tu penses vraiment que c'est équivalent à mes pierres ?",
                       "Hermes – Je n'a rien d'autre à t'échanger.",
                       "Poséidon – Ha ha ha j'en était sur ! Si tu veux mes pierres, trouve donc mon trident, je l'ai perdu quelque part dans l'océan.",
                       "*défaite, retour au début du niveau*"]
    return dialogue_objet

#si le joueur n'a ramasse aucun objet durant le niveau 
dialogue_no = ["Hermes – Je n'ai rien à t'échanger.",
                "Poséidon – Ha ha ha j'en était sur ! Si tu veux mes pierres, trouve donc mon trident, je l'ai perdu quelque part dans l'océan.",
                "*défaite, retour au début du niveau*"]

#si le joueur recommence le niveau, il ne revoit pas le speech du debut 
dialogue_recom = ["Poséidon – Tu en a mis du temps."] 
        
#l objet que hermes ramene a la fin du niveau
#ce ne sont que des teste, il faudra les import depuis le niveau concerné, faire en sorte que 1 seul des 3 soit true 
objet_trident = True
objet_fork = False
objet_peanut = False

#si le joueur a recommencé le niveau (il ne se retappe pas tout le speech du debut), a import du niveau egalement
recommence = False

#general setup
pygame.init() #always need for any kind of pygame code 
clock = pygame.time.Clock()

#setting up the main window 
screen_width = 1080
screen_height = 704 #960
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../../design/niveau2/background.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()
light_grey = (200, 200, 200)
black = (0,0,0)
yellow = (230, 219, 65)
pygame.display.set_caption('poseidon') #the title of the window 

#Scenery
olympeGroup = pygame.sprite.Group()
poseidon = Scenery(0.55, 0.13, 0.35, 0.6, ["../../design/niveau2/poseidon.png"])
olympeGroup.add(poseidon)

hermes = Scenery(0.2, 0.40, 0.10, 0.3, ["../../design/hermes/stand/hermes_s.png"])
olympeGroup.add(hermes)

#text variables
game_font = pygame.font.Font("freesansbold.ttf", 25) #le font et la taille du texte 
zone_text = pygame.Rect(0, screen_height-(screen_height/4), screen_width , screen_height/4) #la zone dans laquelle il y aura le texte 
bouton_suivant = pygame.Rect(screen_width-90, screen_height-50, 70, 30)

counter = 0 #aide a savoir si on est a la fin du message 
speed = 2 #on a 1 caract tous les 2 tics 
active_message = 0 #l indice du message 
active_mess_objets = -1
done = False

if not recommence: #le message du debut differe si il recommence me niveau ou non 
    message = dialogue_all[active_message] #le message actuel
else:
    message = dialogue_recom[0]

#score timer 
score_time = True

while True: #the loop 

    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):
        done = True 
    
    for event in pygame.event.get(): #any movement or intercation or action
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        
        #si on presse entrer on passe au texte suivant 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and not recommence and active_message < len(dialogue_all) -1: #si il est a son premier coup 
                active_message += 1
                done = False 
                message = dialogue_all[active_message]
                counter = 0
            
            else: #texte suivant selon l'objet ramasse 
                #si le joueur a ramassé le trident
                if event.key == pygame.K_RETURN and done and objet_trident and active_mess_objets < len(dialogue_lyre) -1:
                    active_mess_objets += 1
                    done = False 
                    message = dialogue_lyre[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé la fourchette
                elif event.key == pygame.K_RETURN and done and objet_fork and active_mess_objets < len(cas(objet1)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet1)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé le beurre de cacahuette  
                elif event.key == pygame.K_RETURN and done and objet_peanut and active_mess_objets < len(cas(objet2)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet2)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur n'a ramassé aucun objet
                elif event.key == pygame.K_RETURN and done and (not objet_peanut and not objet_fork and not objet_trident) and active_mess_objets < len(dialogue_no) -1:
                    active_mess_objets += 1
                    done = False 
                    message = dialogue_no[active_mess_objets]
                    counter = 0
                    
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

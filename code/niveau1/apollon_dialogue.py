# -*- coding: utf-8 -*-
"""
la cinematique de niveau 1 avec apollon 
"""

import pygame, sys
sys.path.append('../global_niveau') 
from sceneryClass import Scenery

#les dialogues
dialogue_all = ["Apollon – Oh non pas toi ! Que fais tu ici mon frère ? Tu es encore venu me voler mes vaches ?",
                "Hermes – Non, je suis venu te demander de la laine.",
                "Apollon – Pourquoi me demande-tu cela ? Tu ne peux pas demander à quelqu'un d'autre ? Je ne suis pas un mouton !",
                "Hermes – Je veux construire un trône, pour devenir le douzième dieu de l'Olympe.",
                "Apollon – Mhooo c'est mignon, tu veux devenir comme ton incroyable et sublime grand frère petit Hermès ? Si tu veux vraiment cette laine il va falloir me donner quelque chose en échange."]  

#les dialogue suivant l'objet, change suivant l'objet qu'hermes a avec lui 
#l'objet utile ui fait passer au niveau suivant 
dialogue_lyre = ["Hermes – J'ai retrouvé ta lyre ! *il joue un morceau avec la lyre* Si tu la veux, il va falloir me donner la laine.",
                "Apollon – Ma lyre ! Je l'avais perdu. C'est d'accord, marché conclu, voici la laine.",
                "Apollon – D'ailleurs, tu as entendu la nouvelle ? Le roi de la poiscaille a perdu sa fourchette. Hahaha. Quel idiot !",
                "*victoire, niveau suivant*"]

#les autres objets 'inutiles' qui font recommencer le niveau 
#attention bien mettre le determinant devant le nom !!
objet1 = "un arc"  
objet2 = "une montre"

def cas(objet): #meme texte suivant l'objet 'inutile'
    dialogue_objet = ["Hermes – Je peux t'échanger " + objet + ".", 
                       "Apollon – Mais je n'en ai rien à faire de ça. Tu n'as pas autre chose ?",
                       "Hermes – Non je n'a rien d'autre.",
                       "Apollon – Alors va retrouver ma lyre, je l'ai perdu il y a quelques jours. Et si tu la retrouves, je te donnerai ce que tu veux.",
                       "*défaite, retour au début du niveau*"]
    return dialogue_objet

#si le joueur n'a ramasse aucun objet durant le niveau 
dialogue_no = ["Hermes – Je n'ai rien à t'échanger.",
                "Apollon – Alors va retrouver ma lyre, je l'ai perdu il y a quelques jours. Et si tu la retrouves, je te donnerai ce que tu veux.",
                "*défaite, retour au début du niveau*"]

#si le joueur recommence le niveau, il ne revoit pas le speech du debut 
dialogue_recom = ["Apollon – Alors tu l'as trouvé ?"]
   
#l objet que hermes ramene a la fin du niveau
#ce ne sont que des teste, il faudra les import depuis le niveau concerné, faire en sorte que 1 seul des 3 soit true 
objet_lyre = True
objet_arc = False
objet_montre = False

#si le joueur a recommencé le niveau (il ne se retappe pas tout le speech du debut), a import du niveau egalement
recommence = False

#general setup
pygame.init() #always need for any kind of pygame code 
clock = pygame.time.Clock()

#setting up the main window 
screen_width = 1080
screen_height = 704 #960
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../../design/niveau1/background.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()
light_grey = (200, 200, 200)
black = (0,0,0)
yellow = (230, 219, 65)
pygame.display.set_caption('apollon') #the title of the window 

#Scenery
olympeGroup = pygame.sprite.Group()
apollon = Scenery(0.6, 0.1, 0.3, 0.6, ["../../design/niveau1/apollon.png"])
olympeGroup.add(apollon)

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
                #si le joueur a ramassé la lyre 
                if event.key == pygame.K_RETURN and done and objet_lyre and active_mess_objets < len(dialogue_lyre) -1:
                    active_mess_objets += 1
                    done = False 
                    message = dialogue_lyre[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé l'arc
                elif event.key == pygame.K_RETURN and done and objet_arc and active_mess_objets < len(cas(objet1)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet1)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé la montre 
                elif event.key == pygame.K_RETURN and done and objet_montre and active_mess_objets < len(cas(objet2)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet2)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur n'a ramassé aucun objet
                elif event.key == pygame.K_RETURN and done and (not objet_montre and not objet_arc and not objet_lyre) and active_mess_objets < len(dialogue_no) -1:
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

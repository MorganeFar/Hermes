# -*- coding: utf-8 -*-
"""
la cinematique de niveau 4 avec hephaistos
"""

import pygame, sys
sys.path.append('../global_niveau') 
from sceneryClass import Scenery

#les dialogues
dialogue_all = ["Héphaistos – Hermès ! Mon vieil ami ! Que fais-tu ici ?",
                "Hermès – Salut Héphaïstos ! J'ai besoin que tu me fabriques quelque chose, le plus vite possible.",
                "Héphaistos - Bien sûr, qu'est-ce qu'il te faut ?",
                "Hermès – Il me faut un trône, le même que les onze dieux de l'Olympe. Je veux devenir le douzième.",
                "Héphaistos – Toi, le douzième dieu de l'Olympe ? Je ne veux pas te décourager mais il va te falloir plus qu'un simple trône pour convaincre Zeus. De plus, je n'ai pas les ingrédients nécessaires.",
                "Hermès – J'ai tout prévu, voilà les ingrédients.",
                "Héphaistos – Tu es déterminé à ce qu'il paraît. Très bien, je peux te faire un trône, mais qu'as-tu à m'offrir en échange ?"]  

#les dialogue suivant l'objet, change suivant l'objet qu'hermes a avec lui 
#l'objet utile ui fait passer au niveau suivant 
dialogue_coeur = ["Hermès – Je te propose un service contre un service. Tu construis mon trône, et je te trouve une épouse. La plus belle d'entre toutes. Aphrodite elle-même.",
                "Héphaistos – Aphrodite ? La déesse de l'amour et de la beauté mariée à un boiteux ? Elle n'acceptera jamais !",
                "Hermès – Fais moi confiance. Une fois que je serai un dieu de l'Olympe je ferai en sorte que vous soyez marié. T'ai-je déjà déçu mon ami ?",
                "Héphaistos – Jamais ! D'accord, marché conclu dieu de la ruse. Cependant, si tu ne honores pas ta part du contrat, je veillerai personnellement à te laisser moisir dans l'un de mes pièges.",
                "*1h plus tard*",
                "Héphaistos – Voilà ton trône Hermès. Je te fais également un cadeau, des chaussures volantes. Tu arriveras en haut du mont Olympe bien plus rapidement avec elles.",
                "Héphaistos – Tu devrais faire attention, il y a une rumeur qui dit que Héra est à ta recherche. Sois prudent.",
                "*victoire, niveau suivant*"]

#les autres objets 'inutiles' qui font recommencer le niveau 
#attention bien mettre le determinant devant le nom !!
service1 = ["Hèrmes – Je t'offre une coupe de cheveux gratuite, faite par mes soins.", "Héphaistos – Euuuuu... Non merci je ne veux pas finir chauve."]
service2 = ["Hèrmes – Je m'occupe personnellement de ton jardin.", "Héphaistos – Mais enfin Hermès, je n'ai même pas de jardin."]

def cas(service): #meme texte suivant l'objet 'inutile'
    dialogue_service = [service[0],
                        service[1],
                       "Hermès – Mince, je ne sais pas quoi t'offrir d'autre en échange.",
                       "Héphaistos – Bon courage, je n'ai besoin de rien. En tous cas repasse quand tu veux, c'est sympa d'avoir de la companie pour une fois.",
                       "*défaite, retour au début du niveau*"]
    return dialogue_service

#si le joueur n'a ramasse aucun objet durant le niveau 
dialogue_no = ["Hermès – Je n'ai rien à t'offrir en échange.",
               "Héphaistos – Bon courage, je n'ai besoin de rien. En tous cas repasse quand tu veux, c'est sympa d'avoir de la companie pour une fois.",
                "*défaite, retour au début du niveau*"]

#si le joueur recommence le niveau, il ne revoit pas le speech du debut 
dialogue_recom = ["Héphaistos – Tiens tu es encore là ? C'est rare une personne qui reste aussi longtemps dans ma forge."]
        
#l objet que hermes ramene a la fin du niveau
#ce ne sont que des teste, il faudra les import depuis le niveau concerné, faire en sorte que 1 seul des 3 soit true 
service_coeur = True
service_coupe = False
service_jardin = False

#si le joueur a recommencé le niveau (il ne se retappe pas tout le speech du debut), a import du niveau egalement
recommence = False

#general setup
pygame.init() #always need for any kind of pygame code 
clock = pygame.time.Clock()

#setting up the main window 
screen_width = 1080
screen_height = 704 #960
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../../design/niveau4/background.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()
light_grey = (200, 200, 200)
black = (0,0,0)
yellow = (230, 219, 65)
pygame.display.set_caption('hephaistos') #the title of the window 

#Scenery
olympeGroup = pygame.sprite.Group()
hephaistos = Scenery(0.6, 0.1, 0.3, 0.6, ["../../design/niveau4/hephaistos.png"])
olympeGroup.add(hephaistos)

hermes = Scenery(0.2, 0.40, 0.10, 0.3, ["../../design/hermes/stand/hermes_s.png"])
olympeGroup.add(hermes)

def objets():
    trone = Scenery(0.3, 0.4, 0.16, 0.32, ["../../design/niveau4/object/trone.png"])
    olympeGroup.add(trone)
    shoes = Scenery(0.45, 0.61, 0.12, 0.1, ["../../design/niveau4/object/chaussure.png"])
    olympeGroup.add(shoes)
    
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
                #si le joueur a ramassé le coeur  
                if event.key == pygame.K_RETURN and done and service_coeur and active_mess_objets < len(dialogue_coeur) -1:
                    active_mess_objets += 1
                    done = False 
                    message = dialogue_coeur[active_mess_objets]
                    counter = 0
                    #on ajoute les objets à partir d'un certain dialogue 
                    if active_mess_objets == 5:
                        objets()
                #si le joueur a ramassé les ciseaux 
                elif event.key == pygame.K_RETURN and done and service_coupe and active_mess_objets < len(cas(service1)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(service1)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé la pelle 
                elif event.key == pygame.K_RETURN and done and service_jardin and active_mess_objets < len(cas(service2)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(service2)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur n'a ramassé aucun objet
                elif event.key == pygame.K_RETURN and done and (not service_jardin and not service_coupe and not service_coeur) and active_mess_objets < len(dialogue_no) -1:
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

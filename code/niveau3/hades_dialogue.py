# -*- coding: utf-8 -*-
"""
la cinematique de niveau 3 avec hades
"""

import pygame, sys

#les dialogues
dialogue_all = ["Hadès – Bonjour Hermès. Que me vaut cette irruption dans mon royaume ? Amènes-tu une âme aux Enfers ?",
                "Hermès – Non, pas aujourd’hui. J'ai besoin de ton aide dieu de la richesse. J'ai besoin d'or.",
                "Hadès – Hmmm... Intéressant. Et pourquoi veux-tu de l'or ?",
                "Hermès – Je veux construire un trône, pour devenir le douzième dieu de l'Olympe.",
                "Hadès – Très intéressant. Je te souhaite bon courage. Mais tu connais les lois divines Hermès, je ne te donnerai ce que tu veux uniquement si tu as quelque chose à m'échanger."]  

#les dialogue suivant l'objet, change suivant l'objet qu'hermes a avec lui 
#l'objet utile ui fait passer au niveau suivant 
dialogue_casque = ["Hermès – J'ai trouvé ton casque, la kunée. Je te propose un échange, l'or contre le casque.",
                   "Hadès – Très bien. Marché conclu. Voilà tout l'or dont tu as besoin pour ton trône.",
                   "Hadès – Si tu peux me rendre un service, va donc rendre visite au forgeron de l'Olympe, il se sent bien seul.",
                   "*victoire, niveau suivant*"]

#les autres objets 'inutiles' qui font recommencer le niveau 
#attention bien mettre le determinant devant le nom !!
objet1 = "un livre"  
objet2 = "une potion"

def cas(objet): #meme texte suivant l'objet 'inutile'
    dialogue_objet = ["Hermes – J' ai trouvé " + objet + ".", 
                       "Hadès – Cet objet ne m'intéresse pas. Pas contre de l'or en tous cas.",
                       "Hermes – Je n'ai rien trouvé d'autre pour l'échange.",
                       "Hadès – Alors c'est moi qui te propose un marché. Je te donnerai de l'or si tu retrouves mon casque, la kunée. Elle est quelque part aux enfers. Bon courage.",
                       "*défaite, retour au début du niveau*"]
    return dialogue_objet

#si le joueur n'a ramasse aucun objet durant le niveau 
dialogue_no = ["Hermès – Je n'ai rien à t'échanger.",
                "Hadès – Alors c'est moi qui te propose un marché. Je te donnerai de l'or si tu retrouves mon casque, la kunée. Elle est quelque part aux enfers. Bon courage.",
                "*défaite, retour au début du niveau*"]

#si le joueur recommence le niveau, il ne revoit pas le speech du debut 
dialogue_recom = ["Hadès – Déjà de retour à ce que je vois."]

class Scenery(pygame.sprite.Sprite):
    def __init__(self, pos_x_coef, pos_y_coef, widthCoef, heightCoef, pics):
        super().__init__()
        self.sprites = []
        self.current_sprite = 0
        self.begin = True 
        self.move = 0
        self.moveX = 1
        for pic in pics:
            self.sprites.append((pygame.transform.scale(pygame.image.load(pic), (screen_width*widthCoef, screen_height*heightCoef))))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x_coef*screen_width, pos_y_coef*screen_height]
        
        
#l objet que hermes ramene a la fin du niveau
#ce ne sont que des teste, il faudra les import depuis le niveau concerné, faire en sorte que 1 seul des 3 soit true 
objet_casque = True
objet_livre = False
objet_potion = False

#si le joueur a recommencé le niveau (il ne se retappe pas tout le speech du debut), a import du niveau egalement
recommence = False

#general setup
pygame.init() #always need for any kind of pygame code 
clock = pygame.time.Clock()

#setting up the main window 
screen_width = 1080
screen_height = 704 #960
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../../design/niveau3/enfer.png")
fond = pygame.transform.scale(background, (screen_width, screen_height))
fond = fond.convert()
light_grey = (200, 200, 200)
black = (0,0,0)
yellow = (230, 219, 65)
pygame.display.set_caption('hades') #the title of the window 

#Scenery
olympeGroup = pygame.sprite.Group()
hades = Scenery(0.55, 0.13, 0.25, 0.6, ["../../design/niveau3/hades.png"])
olympeGroup.add(hades)

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
                #si le joueur a ramassé le casque 
                if event.key == pygame.K_RETURN and done and objet_casque and active_mess_objets < len(dialogue_casque) -1:
                    active_mess_objets += 1
                    done = False 
                    message = dialogue_casque[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé le livre
                elif event.key == pygame.K_RETURN and done and objet_livre and active_mess_objets < len(cas(objet1)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet1)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur a ramassé la potion 
                elif event.key == pygame.K_RETURN and done and objet_potion and active_mess_objets < len(cas(objet2)) -1:
                    active_mess_objets += 1
                    done = False 
                    dialogue_obj = cas(objet2)
                    message = dialogue_obj[active_mess_objets]
                    counter = 0
                #si le joueur n'a ramassé aucun objet
                elif event.key == pygame.K_RETURN and done and (not objet_potion and not objet_livre and not objet_casque) and active_mess_objets < len(dialogue_no) -1:
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

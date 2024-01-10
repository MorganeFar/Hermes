"""
welcome 
"""

# ---------------- IMPORTATIONS ----------------
from settings import screen_height, screen_width, hermes_logo, play_button, menu_bg
import sys, pygame
from sceneryClass import Scenery
# ----------------------------------------------

pygame.init()
clock = pygame.time.Clock()

### WINDOW ###
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Welcome')


### SCENERY ###
welcomeGroup = pygame.sprite.Group()
background = pygame.image.load(menu_bg[0]) # Le fond 
background = pygame.transform.scale(background,(screen_width,screen_height))

# Le titre 
TITLE_POS_X_COEF = 0.15
TITLE_POS_Y_COEF = 0.15
TITLE_WIDTH_COEF = 0.7
TITLE_HEIGHT_COEF = 0.3
title = Scenery(TITLE_POS_X_COEF, TITLE_POS_Y_COEF,TITLE_WIDTH_COEF, TITLE_HEIGHT_COEF, hermes_logo)

# Le bouton play
PLAY_POS_X_COEF = 0.345
PLAY_POS_Y_COEF = 0.53
PLAY_WIDTH_COEF = 0.3
PLAY_HEIGHT_COEF = 0.2
play = Scenery(PLAY_POS_X_COEF, PLAY_POS_Y_COEF, PLAY_WIDTH_COEF, PLAY_HEIGHT_COEF, play_button)

welcomeGroup.add(title, play)

def welcomeMenu():
    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Ferme la fenetre/ jeux
                sys.exit() # Arrête tout le programme

            # Si on clique sur le bouton play, on commmence le jeu
            if event.type == pygame.MOUSEBUTTONDOWN:
                posMouse = pygame.mouse.get_pos()
                minX = PLAY_POS_X_COEF * screen_width
                maxX = minX + screen_width * PLAY_WIDTH_COEF
                minY = PLAY_POS_Y_COEF * screen_height
                maxY = minY + screen_height * PLAY_HEIGHT_COEF
                if ( minX <= posMouse[0] <= maxX
                    and minY <= posMouse[1] <= maxY):
                    # PERMET DE LANCER LE NIVEAU 1
                    return 'start'

            # Si on clique sur entrer, on commence le jeu 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'start'
            
        
        # Logic
        play.zoom()
        play.update(0.030, 1.9) 
        
        screen.blit(background,(0,0))
        welcomeGroup.draw(screen)
       
        pygame.display.flip()
        clock.tick(60) # Controle la vitesse de maj
        

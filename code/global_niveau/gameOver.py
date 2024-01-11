# -*- coding: utf-8 -*-
"""
game_over
"""

# ---------------- IMPORTATIONS ----------------
import pygame, sys
sys.path.append("../niveau1")
from sceneryClass import Scenery
from settings import screen_height, screen_width, replay_button, game_over_logo, charon_pic
# ----------------------------------------------

pygame.init()
clock = pygame.time.Clock()

# Window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Over')

# Scenery
gameOverGroup = pygame.sprite.Group()
background = pygame.Color((39, 9, 63))  # Le fond
gameOver = Scenery(0.35, 0.06, 0.3, 0.3, game_over_logo)  # Le logo game_over
gameOverGroup.add(gameOver)

# Mise en place de Charon 
charon = Scenery(0.57, 0.69, 0.3, 0.3, charon_pic)
gameOverGroup.add(charon)

# Les emplacements du bouton retry pour cliquer dessus 
RETRY_POS_X_COEF = 0.4
RETRY_POS_Y_COEF = 0.43
RETRY_WIDTH_COEF = 0.2
RETRY_HEIGHT_COEF = 0.15

# Mise en place du bouton retry
retry = Scenery(RETRY_POS_X_COEF, RETRY_POS_Y_COEF, RETRY_WIDTH_COEF, RETRY_HEIGHT_COEF, replay_button)
gameOverGroup.add(retry)

# Le status du joueur 
status = 'dead'


def over():
    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Ferme la fenetre/ jeux
                sys.exit()  # Arrête tout le programme

            # Si on appuie sur entrer on retrourne sur l'overworld  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    status = 'overworld'
                    return status

            # Si on clique sur le bouton retry on retrourne sur l'overworld
            if event.type == pygame.MOUSEBUTTONDOWN:
                posMouse = pygame.mouse.get_pos()
                minX = RETRY_POS_X_COEF * screen_width
                maxX = minX + screen_width * RETRY_WIDTH_COEF
                minY = RETRY_POS_Y_COEF * screen_height
                maxY = minY + screen_height * RETRY_HEIGHT_COEF
                if ( minX <= posMouse[0] <= maxX
                    and minY <= posMouse[1] <= maxY):
                    status = 'overworld'
                    return status  # Pour revenir dans l'overworld => sortir de la fonction

        # Logic
        charon.move_left()  # Charon se deplace
        retry.zoom()  # Le bouton retry zoom et dezoom
        charon.update(0.008, 1)
        retry.update(0.015, 1.9)
                
        screen.fill(background)
        gameOverGroup.draw(screen)
    
        pygame.display.flip()
        clock.tick(60)  # Controle la vite de mise a jour

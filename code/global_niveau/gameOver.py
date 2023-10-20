# voir pour faire un bouton https://openclassrooms.com/forum/sujet/bouton-cliquable-pygame
# https://www.codingninjas.com/studio/library/create-the-buttons-in-a-game-using-pygame
import pygame, sys
sys.path.append("../niveau1")
from mainCode import *
from sceneryClass import Scenery
from settings import screen_height, screen_width, replay_button, game_over_logo, charon_pic
        

pygame.init()
clock = pygame.time.Clock()

#Window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Over')


#Scenery
gameOverGroup = pygame.sprite.Group()
background = pygame.Color((39, 9, 63))
gameOver = Scenery(0.35, 0.06, 0.3, 0.3, game_over_logo)
gameOverGroup.add(gameOver)

charon = Scenery(0.57, 0.69, 0.3, 0.3, charon_pic)
gameOverGroup.add(charon)

RETRY_POS_X_COEF = 0.4
RETRY_POS_Y_COEF = 0.43
RETRY_WIDTH_COEF = 0.2
RETRY_HEIGHT_COEF = 0.15

retry = Scenery(RETRY_POS_X_COEF, RETRY_POS_Y_COEF, RETRY_WIDTH_COEF, RETRY_HEIGHT_COEF, replay_button)
gameOverGroup.add(retry)


def over():
    while True:
        #Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #ferme la fenetre/ jeux
                sys.exit() #arrête tout le programme
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                posMouse = pygame.mouse.get_pos()
                minX = RETRY_POS_X_COEF * screen_width
                maxX = minX + screen_width * RETRY_WIDTH_COEF
                minY = RETRY_POS_Y_COEF * screen_height
                maxY = minY + screen_height * RETRY_HEIGHT_COEF
                if ( minX <= posMouse[0] <= maxX
                    and minY <= posMouse[1] <= maxY):
                    level.isDead = False
                    start()
            
        # logic
        charon.move_left()
        retry.zoom()
        charon.update(0.008, 1)
        retry.update(0.015, 1.9)
                
        screen.fill(background)
        gameOverGroup.draw(screen)
    
        pygame.display.flip()
        clock.tick(60)# controle la vite de maj
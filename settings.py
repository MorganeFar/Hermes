
###### MAPS #####

tile_size = 64 #100

# LEVEL 1 
level_map = [
'                                                                                                                    ',
'                                                                                                                    ',
'                                                              XXXX   X                                              ',
'                                                                                                 XX                 ',
'           X                          XX                  XX                                                XXX     ',
'      P                                                                                      XX                     ',
'      XX    XXXX               XXX            XXXXXX          XX          XXXXXXX                     XXXX          ',
'       X                                           X                  X      X           XXXXX                      ',
'  XX   X                    XX            XX       X      XX       X  X      X           X                          ',
'       X                                           X               X  XX     X         XXX                          ',
'XXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXX    XXXXXXXXXXXXXX  XXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXX']

# LEVEL 2

level_map_nv2 = [
'                          ',
'                          ',
'        XXXXXXXXXX        ',
'                          ',
'                      XX  ',
'      P                   ',
'      XX    XXXX          ',
'       X                  ',
'  XX   X                  ',
'       X                  ',
'XXXXXXXXXXXXXXXX  XXXXXXXX']


##### SCREEN #####
screen_width = 1080
screen_height = len(level_map) * tile_size #pas plus de 700

#### PICTURES PATHS TABLES ####

## Backgrounds ##
menu_bg = ["HermesDesigns/Menu/Begin/background.png"]

## Logos ##
hermes_logo = ["HermesDesigns/Menu/Begin/title.png"]
game_over_logo = ["HermesDesigns/Menu/Over/game_over.png"]

## Characters ##
charon_pic = ["HermesDesigns/Menu/Over/charon.png"]
cloud_pic = ["HermesDesigns/Global/cloud.png"]
sun_pic = ["HermesDesigns/Menu/Begin/sun_1.png", "HermesDesigns/Menu/Begin/sun_2.png"]

## HERMES ##
hermes_stand = ["HermesDesigns/Hermes/idle/hermes_s.png"]
hermes_run = ["HermesDesigns/Hermes/run/hermes_r1.png", "HermesDesigns/Hermes/run/hermes_r2.png", "HermesDesigns/Hermes/run/hermes_r3.png", "HermesDesigns/Hermes/run/hermes_r4.png"]
hermes_jump = ["HermesDesigns/Hermes/jump/hermes_j.png"]
hermes_swim = ["HermesDesigns/Hermes/swim/hermes_sw1.png", "HermesDesigns/Hermes/swim/hermes_sw2.png", "HermesDesigns/Hermes/swim/hermes_sw3.png"]

## Buttons ##
play_button = ["HermesDesigns/Menu/Begin/play.png", "HermesDesigns/Menu/Begin/play_bigger.png"]
replay_button = ["HermesDesigns/Menu/Over/retry.png", "HermesDesigns/Menu/Over/retryBigger.png"]
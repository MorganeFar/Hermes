# -*- coding: utf-8 -*-
"""
player
"""
# ---------------- IMPORTATIONS ----------------
import pygame 
from support import import_folder 
from math import sin
from settings import screen_width
# -----------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_health, level_data):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 # Indice de l'image pour l'animation 
        self.level_data = level_data    # Donnees du niveau
        self.noLevel = self.level_data['unlock'] - 1    # Numero du niveau actuel
        self.animation_speed = self.level_data['animation_speed']  # Vitesse de l'animation

        # Recuperation du personnage Hermes
        # Rotation permettant d'avoir Hermes couche si besoin
        self.image = pygame.transform.rotate(self.animations[self.level_data['status']][self.frame_index], self.level_data['rotation'])
        self.rect = self.image.get_rect(topleft=pos)
        
        # Deplacement du joueur
        self.direction = pygame.math.Vector2(0,0)   # Vecteur direction du joueur
        self.speed = self.level_data['speed']   # Vitesse de deplacement
        self.gravity = self.level_data['gravity']   # Gravite applique
        self.jump_speed = self.level_data['jump_speed']  # Hauteur des sauts
        
        # Statut du joueur
        self.status = self.level_data['status']     # Statut du joueur au debut du niveau
        self.facing_right = True  # Joueur dirige vers la droite

        # NIVEAU 3 SEULEMENT
        # Sens inverse
        if self.noLevel == 3: self.facing_right = not self.facing_right

        # NIVEAU 5 SEULEMENT
        self.NoNiveau = self.level_data['NoNiveau']
        if self.NoNiveau == 5:
            self.rect = self.image.get_rect(midbottom=pos)  # Adaptation position du joueur (ne commence pas a gauche)
            # Empeche le joueur d'aller plus loin que l'ecran visible sur les cotes
            self.max_x_constraint = screen_width
        
        # Placement propre des retangles
        self.on_ground = False 
        self.on_ceiling = False 
        self.on_left = False 
        self.on_right = False 
        
        # Gestion de la 'sante' du joueur
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0  # Nombre de fois que le joueur s'est fait touche
        
        # Audio associe au saut
        if self.noLevel == 2:
            self.jump_sound = pygame.mixer.Sound('../../audio/swim.ogg')
        else:
            self.jump_sound = pygame.mixer.Sound('../../audio/jump.wav')
            self.jump_sound.set_volume(0.1)
        
    def import_character_assets(self):
        # Recuperation des images du personnage
        character_path = '../../design/hermes/'
        self.animations = {'stand': [], 'run': [], 'jump': [], 'fly': [], 'swim': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = import_folder(full_path)

    # Recuperation du status du personnage pour l'animer en consequence
    def animate(self):
        animation = self.animations[self.status]
        
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):  # si on depasse la taille du tableau on revient au debut
            self.frame_index = 0

        # Applique la bonne image et la bonne rotation de celle-ci en continue
        image = pygame.transform.rotate(animation[int(self.frame_index)], self.level_data['rotation'])

        if self.facing_right:  # Si on va vers la droite on tourne pas les images
            self.image = image
        else:  # Retrourne les images si on va vers la gauche
            flipped_image = pygame.transform.flip(image, True, False)  # flip(picture, horizontaly(x), verticaly(y))
            self.image = flipped_image

        # Cas ou le personnage es tinvincible temporairement 
        if self.invincible:
            alpha = self.wave_value() 
            self.image.set_alpha(alpha) # Fait en sorte que le perso clignotte 
        else:
            self.image.set_alpha(255)

        # Repositionne le personnage dans toutes les situations possibles => enleve certains bugs
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            self.on_ceiling = False

        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.on_ceiling = False

        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.on_ceiling = False

        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
            self.on_ground = False

        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            self.on_ground = False

        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
            self.on_ground = False

    # Deplacement du personnage suivant les touches entrees
    def get_input(self):
        keys = pygame.key.get_pressed()  # Recupere l'ensemble des touches pressees

        # Mouvement horizontaux

        if self.noLevel == 3:
            if keys[pygame.K_LEFT]:  # Deplacement vers la droite avec la fleche de gauche
                self.direction.x = 1
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:  # Deplacement vers la gauche avec la fleche de droite
                self.direction.x = -1
                self.facing_right = True
            else:
                self.direction.x = 0

        # Cas particulier niveau 5 : deplacement limite vers la droite et la gauche
        elif self.NoNiveau == 5:
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed 
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.speed 
                self.facing_right = False

        # Autres niveaux (1, 2, 4)
        else:
            if keys[pygame.K_RIGHT]:  # Deplacement vers la droite
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:  # Deplacement vers la gauche
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

        # Saut
        if self.noLevel == 2:
            # Pour monter dans l'eau => pas besoin de toucher le sol
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jump()
                self.on_ground = False
        # Pas de saut possible dans le niveau 5
        elif self.NoNiveau == 5:
            pass
        else:
            # Le joueur peut sauter que s'il est sur le sol
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground and self.noLevel != 3:
                self.jump()
                self.on_ground = False  # Lorsqu'il saut il n'est plus sur le sol
            # Cas particulier niveau 3 : gravite inversee
            elif (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ceiling and self.noLevel == 3:
                self.jump()
                self.on_ceiling = False

    # Recupere le statut du joueur (jump, stand, run, ...)
    def get_status(self):
        keys = pygame.key.get_pressed()  # Recupere l'ensemble de touche clavier pressees

        if self.noLevel != 2:
            if self.NoNiveau != 5:
                if self.direction.y < 0:  # Si le joueur va vers le haut alors il saute
                    self.status = 'jump'
                elif self.direction.y > 1:  # si joueur va vers le bas alors il est debout
                    self.status = 'stand'  # ou s'il tombe
                else:
                    if self.direction.x != 0:  # si le joueur va a droite ou a gauche alors il court
                        self.status = 'run'
                    else:   # S'il ne se deplace pas horizontalement alors il est debout
                        self.status = 'stand'

        elif self.noLevel == 2:
            # Niveau 2 => Nage seulement
            if (self.direction.x != 0 or keys[pygame.K_RIGHT] or
                    keys[pygame.K_LEFT] or keys[pygame.K_SPACE]):
                self.status = 'swim'

    # Gravite applique au joueur
    def apply_gravity(self):
        # Permet de retomber apres un saut
        self.direction.y += self.gravity  # Gravite applique à la verticale
        self.rect.y += self.direction.y

    # Fait sauter le joueur
    def jump(self):
        self.direction.y = self.jump_speed  # Applique un saut d'une hauteur donnee
        self.jump_sound.play()

    # Le joueur se fait toucher
    def get_damage(self):
        if not self.invincible:
            self.change_health(-1)  # <=> change_health -= 1
            self.invincible = True  # Ne peut pas se faire retoucher pendant une courte periode
            self.hurt_time = pygame.time.get_ticks()

    # Calcul de temps d'invicibilite
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    # Permet d'avoir le clignottement du joueur quand il est invincible 
    def wave_value(self):
        value = sin(pygame.time.get_ticks()) # On utilise la sonction sinus pour créer 2 états différents pour le clignottement 
        if value >= 0: return 255
        else: return 0

    # Limite le terrain du joueur pour le niveau 5
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Mise a jour du joueur
    def update(self):
        self.get_input()    # Ecoute les touches pressees par le joueur
        self.get_status()   # Recupere le statut du joueur
        self.animate()      # Anime le joueur en fonction des resultats precedent
        if self.NoNiveau == 5:
            self.constraint()
        self.invincibility_timer()  # Gere le chronometre suite a une perte de vie
        self.wave_value()
        

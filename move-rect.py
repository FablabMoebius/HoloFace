'''
[En] This Script tests animation of "pixels" through rectangles in pygame. If the animation quality is not good enough we will explore another way to obtain a smooth animation
[Fr] Ce script teste l'animation des "pixels" via les rectangles de PyGame. Si le résultat n'est pas assez qualitatif, on essayera un autre moyen.
'''
import sys, time, random
import pygame as pg
import os
path = os.getcwd()

#----------------------------------------------------------
# [En] Variables & inits
# [Fr] Variables et Initialisations
#----------------------------------------------------------

#[En] / [Fr] Pygame
pg.init()

# [En] Size of TV screen
# [Fr] Taille de l'écran télé

screen_w = 500
screen_h = 500

holoface_close = False

# Colors  / Couleurs
marine = (0, 10, 50)
white = (255,255,255)

# pixel - position
x = 100
y = 100
# pixel target position
target_x = 150
target_y = 150
# Motion step / Pas de l'animation
pas_x = int((target_x-x)/24)
pas_y = int((target_y-y)/24)
# Clock init for FPS specification / Initialisation de l'horloge pour déterminer la fréquence de l'affichage
clock = pg.time.Clock()

#----------------------------------------------------------
# [En] Functions
# [Fr] Fonctions
#----------------------------------------------------------

def main(holoface_close,x,y,target_x,target_y):
    # [En] Window creation
    # [Fr] Creation de la fenêtre
    screen = pg.display.set_mode((screen_w, screen_h))
    screen.fill(marine)
    pg.display.flip()
    pg.display.set_caption('HoloFace')
    pg.mouse.set_visible(0)

    # [En] Prevent python window from closing
    # [Fr] Bloque la fermeture de la fenêtre
    while not holoface_close:
        for event in pg.event.get():
            if event.type == pg.QUIT :
                holoface_close = True
                pg.quit()

        # [En] Motion test
        # [Fr] Test de déplacement

        t_reached = True

        if x >= target_x :
            t_reached = False
        else:
            # [En] Motion step increment
            # [Fr] Incrément du pas de déplacement
            x += 2

        screen.fill(marine)
        monrect = pg.draw.rect(screen, white, pg.Rect(x, y, 50, 50))

        pg.display.update()
        pg.display.flip()

        # [En] Frame rate definition
        # [Fr] Définition de la fréquence de l'animation
        clock.tick(24)

#----------------------------------------------------------
# [En] Main program
# [Fr] Programme principal
#----------------------------------------------------------
main(holoface_close,x,y,target_x,target_y)
pg.quit()
quit()
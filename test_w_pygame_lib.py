'''
[En]
FABLAB MOEBIUS - 6/8/19
Holoface Project - Maker Faire Paris 2019
Authors : Henry Proudhon & Villafruela Naimeric

[Fr]
FABLAB MOEBIUS - 8/6/19
Projet HoloFace - Maker Faire Paris 2019
Auteurs : Henry Proudhon & Villafruela Naimeric
'''

#----------------------------------------------------------
# [En] Library import
# [Fr] Imporation des librairies
#----------------------------------------------------------

import sys, time, random
import pygame as pg
import os
path = os.getcwd()
pg.init()

#----------------------------------------------------------
# [En] VARIABLES & INITS
# [Fr] VARIABLES & INITIALISATIONS
#----------------------------------------------------------

# [En]
# SCREEN
# Orientation mode of the screen : (v) for vertical / (h) for horizontal

# [Fr]
# ECRAN
# Choix du mode d'orientation de l'ecran : Mode vertical (v) ou Horizontal (h)

mode = 'v'

# Default screen dimensions
# Dimensions de l'ecran (Le format de base est un écran full HD
# 1 = taille d'un écran full HD (1920 x 1080) / 2 = moitiée d'un écran Full HD / 3 = tiers d'un écran Full HD
ratio = 2

if (mode == 'v'):
    screen_w = int(1080/ratio)
    screen_h = int(1920/ratio)
    col_max = int(36/ratio)  # nombre max de colonne dispo en fonction du pas horizontal et de la largeur de l'écran
    line_max = int(64/ratio)  # nombre max de ligne dispo en fonction du pas vertical et de la hauteur de l'écran
elif (mode == 'h'):
    screen_w = int(1920/ratio)
    screen_h = int(1080/ratio)
    col_max = int(64/ratio)  # nombre max de colonne dispo en fonction du pas horizontal et de la largeur de l'écran
    line_max = int(36/ratio) # nombre max de ligne dispo en fonction du pas vertical et de la hauteur de l'écran
# definition de l'écran
screen = pg.display.set_mode((screen_w,screen_h))
screen.fill((0,10,50))
pg.display.update()
pg.display.set_caption('HoloFace')
pg.mouse.set_visible(0)

bgd_color = pg.Color(0,10,50,255) # Marine Blue

# Pas horizontal et vertical pour le placement des carres (en pixels)
step_h = 30 #pixels
step_v = 30 #pixels


#Caracteristiques des pixels (width, height)
pixel_w = 5 #pixels
pixel_h = 5 #pixels
# initial % scale
pixel_scale = 10 #en pourcentage
# Délai maximum entre génération de vagues
delay_max = 1

holoface_close = False

# COULEURS
# Parametres du fond de l'ecran

# Couleur des pixels
pixel_color = 'white'
line_color = (0,2,80)

# Colonnes
for i in range (1,col_max):
    pg.draw.line(screen,(0,20,80),(i*step_h,0),(i*step_h,screen_h),1)
    pg.display.update()
# Lignes
for i in range (1,line_max):
    pg.draw.line(screen,(0,20,80),(0,i*step_v),(screen_w,i*step_v),1)
    pg.display.update()

# rectangles
for l in range (1, line_max):
        for i in range (1, col_max):
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(int(i*step_h),int(l*step_v),int(pixel_w*pixel_scale/100),int(pixel_h*pixel_scale/100)))
            #print('pox x : %d, pos y : %d, pos x + pixw : %d, pos y + pixh : %d' % (i*step_h,l*step_v,i*step_h+pixel_w,l*step_v+pixel_h))
pg.display.update()



pg.transform.scale (pg.image.load(path+'/images/shim.png'), [10,10])
pg.display.update()

# On bloque la fermeture de la fenêtre
while not holoface_close:
        for event in pg.event.get():
                if event.type == pg.QUIT :
                    holoface_close = True
                    pg.quit()

#def main ():

#main()
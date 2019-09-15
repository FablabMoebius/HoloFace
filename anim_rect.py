# coding: utf-8
'''
[En] test rectangle animation
'''
import sys, time, random
import pygame as pg
import os
import numpy as np
from math import sin, pi
import time
from scipy import ndimage

def RoundedRect(screen, rect, color, radius=0.5, angle=0):
    """
    :param screen: display destination
    :param rect: pygame Rect instance
    :param color: color in rgb or rgba mode
    :param float radius: rounded corner ratio in [0, 1]
    :param int angle: rotation angle in degrees
    """

    color = pg.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pg.Surface(rect.size, pg.SRCALPHA)

    circle = pg.Surface([min(rect.size) * 3] * 2, pg.SRCALPHA)
    pg.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pg.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
    rectangle.fill(color, special_flags=pg.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MIN)
    r = pg.transform.rotate(rectangle, angle)

    return screen.blit(r, pos)

def f(t):
    """Time function to pace the animation."""
    return np.abs(np.sin(pi * t / T))

def triangle(t):
    """Linear time function to rotate the pattern forth and back."""
    return 2 * np.abs(t / T - np.floor(t / T + 0.5))

def load_image(im_name):
    # read the image using pyplot
    from matplotlib import pyplot as plt
    im = plt.imread(os.path.join('images', im_name))
    if im.ndim == 3:
        im = im[:, :, 0]
    return im / im.max()  # normalize image

path = os.getcwd()
holoface_close = False  # flag to stop the game
pg.init()

# animation parameters
anim = 'splash'  # must be in ['random', 'splash', image']
save_screenshot = False
fps = 40  # frame per second
N_ROWS_DEFAULT = 30
N_COLS_DEFAULT = 30
SIZE = 15  # size of a square unit [pixel]
T = 10  # animation period [s]
rot_angle = 180  # degrees, angle to rotate the target as time increases
tilt_angle = 45  # degrees, angle to give a sense of depth

'''
# plot the time functions for debugging
from matplotlib import pyplot as plt
t = np.linspace(0, 20, 501)
plt.figure()
plt.plot(t, f(t))
plt.plot(t, triangle(t))
plt.show()
'''

# colors
marine = (0, 10, 50)
white = (255, 255, 255)

# construct the target pattern which is used to control the sizes and the angles
if anim == 'random':
    # here we use randomly distributed values for the animation
    target = np.random.uniform(0, 1, N_ROWS_DEFAULT * N_ROWS_DEFAULT).reshape((N_ROWS_DEFAULT, N_ROWS_DEFAULT))
elif anim == 'splash':
    # load the logo
    im_name = 'holoface_ambigram_60x60.png'
    #target = load_image('holoface_ambigram_100x38.png')
    target = load_image(im_name)
    rot_angle = 180.
    tilt_angle = 0.
elif anim == 'image':
    target = load_image('hp_50x60.png')
    rot_angle = 0.
    tilt_angle = 45.
else:
    print('wrong animation type: %s' % anim)
    holoface_close = True
# now get the actual N_ROWS, N_COLS values from the target
N_ROWS, N_COLS = target.shape

# setup the screen
screen = pg.display.set_mode((N_COLS * SIZE, N_ROWS * SIZE))
screen.fill(marine)
pg.display.set_caption('HoloFace test animation')
pg.mouse.set_visible(0)

clock = pg.time.Clock()  # setup clock
#t0 = clock.get_time()
t0 = time.time()

ones = np.ones((N_ROWS, N_COLS), dtype=float)
sizes = ones
# angle should evolve between zero (low grey values) and 45 deg (highest gray values)
angles = np.zeros((N_ROWS, N_COLS), dtype=float)
# compute mean coordinates once and for all
xy = np.empty((2, N_ROWS, N_COLS), dtype=int)
for i in range(N_ROWS):
    for j in range(N_COLS):
        xy[0, i, j] = (2 * j + 1) * (SIZE // 2)
        xy[1, i, j] = (2 * i + 1) * (SIZE // 2)
print(xy[0].shape)

while not holoface_close:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            holoface_close = True
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.Q:  # use 'Q' to quit game
                holoface_close = True
                break
    
    t = time.time()
    screen.fill(marine)  # clear screen
    # rotate the target if needed
    rot_target = ndimage.rotate(target, rot_angle * triangle(t - t0), reshape=False)

    # compute all sizes and angles for this time increment
    sizes = np.maximum(rot_target * 10 * f(t - t0), ones)  # use a minimum size of 1
    #angles = np.zeros((N_ROWS, N_COLS), dtype=float)
    angles = rot_target * -tilt_angle * f(t - t0)
    # draw all rectangle using list comprehension (avoid for loops for performance)
    [RoundedRect(screen, pg.Rect(xy[0, i, j] - sizes[i, j] // 2, 
                                 xy[1, i, j] - sizes[i, j] // 2, 
                                 sizes[i, j], sizes[i, j]), 
                                 white, 0.5, angles[i, j]) for j in range(N_COLS) for i in range(N_ROWS)]
    pg.display.update()
    clock.tick(fps)

print('thank you for playing')
if save_screenshot:
    pg.image.save(screen, os.path.join('images', 'screenshot.bmp'))
time.sleep(0.2)
pg.display.quit()


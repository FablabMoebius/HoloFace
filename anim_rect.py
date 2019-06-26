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

#"""
path = os.getcwd()
pg.init()

# animation parameters
fps = 100  # frame per second
N_ROWS = 30
N_COLS = 40
SIZE = 25  # size of a square unit [pixel]
size_init = SIZE // 5  # initial shape size [pixel]
T = 5  # resize period [s]
rotation_speeds = np.random.uniform(0, 1, N_ROWS * N_COLS).reshape((N_ROWS, N_COLS))
print(rotation_speeds)

marine = (0, 10, 50)
white = (255, 255, 255)

screen = pg.display.set_mode((N_COLS * SIZE, N_ROWS * SIZE))
screen.fill(marine)
pg.display.flip()
pg.display.set_caption('HoloFace test animation')
pg.mouse.set_visible(0)

holoface_close = False  # flag to stop
clock = pg.time.Clock()
t0 = clock.get_time()
print(t0)
t0 = time.time()
print(t0)

sizes = size_init * np.ones((N_ROWS, N_COLS), dtype=float)
angles = np.zeros((N_ROWS, N_COLS), dtype=float)

while not holoface_close:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            holoface_close = True
            pg.quit()
    
    t = time.time()
    rect = pg.draw.rect(screen, marine, pg.Rect(0, 0, N_COLS * SIZE, N_ROWS * SIZE))
    for i in range(N_ROWS):
        for j in range(N_COLS):
            x, y = (2 * j + 1) * SIZE // 2, (2 * i + 1) * SIZE // 2
            sizes[i, j] = size_init + rotation_speeds[i, j] * SIZE // 2 * abs(sin(pi * (t - t0) / T))
            angles[i, j] = (angles[i, j] + rotation_speeds[i, j]) % 360  # rotation angle
            size = sizes[i, j]
            RoundedRect(screen, pg.Rect(x - size // 2, y - size // 2, size, size), white, 0.5, angles[i, j])
    pg.display.update()
    clock.tick(fps)
#"""
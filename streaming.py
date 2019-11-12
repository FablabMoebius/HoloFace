# coding: utf-8
import sys, time, random
import pygame as pg
import os
import numpy as np
from math import floor
from animate import square

class Stream():

    def __init__(self, col=0):
        self.active = False
        self.col = col
        self.row = 0

    def __repr__(self):
        out = 'Stream at (%d, %d), Active=%s' % (self.col, self.row, self.active)
        return out

N_COLS = 50
N_ROWS = 50
SIZE = 15
STREAM_LENGTH = 11  # number of rows that spans a stream
DS = 0.5  # second, time sparating two streams
VELOCITY = 100  # pixel / second
FPS = 10
save_screenshot = True

def blit_shape(surface, rect, color):
    """
    :param surface: Surface instance destination
    :param rect: pygame Rect instance
    :param color: color in rgb or rgba mode
    """
    rectangle = shape(rect.size[0], color)
    return surface.blit(rectangle, rect.topleft)

def streaming():
    """Streaming animation while the program is not being used."""
    streaming_close = False  # flag to stop the animation
    pg.init()
 
    # colors
    marine = (0, 10, 50)
    white = (255, 255, 255)

    # setup the screen
    screen = pg.display.set_mode((N_COLS * SIZE, N_ROWS * SIZE))
    screen.fill(marine)

    pg.display.set_caption('HoloFace test animation')
    pg.mouse.set_visible(0)

    pg.display.update()  # to display the background

    clock = pg.time.Clock()  # setup clock
    t0 = pg.time.get_ticks()  # in ms
    last_t = t0
    last_s = -1
    streams = [Stream(i) for i in range(N_COLS)]  # inactive list of N_COLS streams

    # main loop executing the animation
    while not streaming_close:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                holoface_close = True
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:  # use 'q' to quit game
                    print('exiting the game')
                    streaming_close = True
                    break
        t = pg.time.get_ticks()  # in ms
        screen.fill(marine)
        # update stream positions
        dt = (t - last_t) / 1000
        for stream in streams:
        	if stream.active == True:
        	    stream.row = stream.row + dt * VELOCITY
        	    if stream.row > (N_ROWS + 0.5 * STREAM_LENGTH) * SIZE:
        	    	# deactivate this stream
        	    	stream.row = 0
        	    	stream.active = False
        	last_t = t
        # a new stream is activated every DS second
        ds = (t - last_s) / 1000
        if ds > DS:
            # activate a new stream
            index = np.random.randint(0, N_COLS, 1)[0]
            print(streams[index])
            streams[index].active = True
            print('activating new stream at t=%.1f in col %d' % (t, streams[index].col))
            last_s = t
        for stream in streams:
            if not stream.active:
                continue
            #blit_shape(screen, pg.Rect(stream.col - SIZE / 2, stream.row - SIZE / 2, SIZE, SIZE), white)
            for i in range(STREAM_LENGTH):
                f = 2 * np.abs(i / 10 - np.floor(i / 10 + 0.5))
                size_i = f * SIZE
                rectangle = square(size_i, white)
                screen.blit(rectangle, (stream.col * SIZE - size_i / 2, stream.row - size_i / 2 - (5 + i) * SIZE))

        pg.display.update()
        clock.tick(FPS)

    print('thank you for playing')
    if save_screenshot is True:
        pg.image.save(screen, os.path.join('images', 'streaming.png'))
        print('screenshot was saved')
    time.sleep(0.2)
    pg.display.quit()

if __name__ == '__main__':
    streaming()
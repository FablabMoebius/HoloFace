# coding: utf-8
import sys, time, random
import pygame as pg
import os
import numpy as np
from math import floor
from animate import square

class Stream():
    """A stream has basically a length and a size function.

    The stream can move acros the screen as time evolves. The position of the stream 
    and its size function is used to compute the size of the blocks.
    """

    STREAM_LENGTH = 31  # odd number of rows that spans a stream
    STREAM_LENGTH_STD = 10
    STREAM_VELOCITY = 100  # pixel / second
    STREAM_VELOCITY_STD = 30

    def __init__(self, col=0, length=None, velocity=None):
        self.active = False
        self.col = col
        if length == None:
            length = self.STREAM_LENGTH
        # ensure length is an odd number
        if length % 2 == 0:
            length += 1
        self.length = length
        self.position = - (self.length - 1) / 2 * SIZE
        if velocity is None:
            velocity = self.STREAM_VELOCITY
        self.velocity = velocity
        # initialize list with size values
        self.sizes = [self.size(i) for i in range(self.length)]

    def __repr__(self):
        out = ['Stream of length %d in column %d' % (self.length, self.col),
               'position = %d pixels, velocity=%d pixel / s' % (self.position, self.velocity),
               'active=%s' % self.active]
        return "\n".join(out)

    def get_head(self):
        return self.position + self.length / 2 * SIZE
        
    def get_tail(self):
        return self.position - self.length / 2 * SIZE

    @staticmethod
    def pick_length():
        return np.random.randint(Stream.STREAM_LENGTH - Stream.STREAM_LENGTH_STD, Stream.STREAM_LENGTH + Stream.STREAM_LENGTH_STD)

    @staticmethod
    def pick_velocity():
        return np.random.randint(Stream.STREAM_VELOCITY - Stream.STREAM_VELOCITY_STD, Stream.STREAM_VELOCITY + Stream.STREAM_VELOCITY_STD)

    def size(self, row):
        i = (row - self.position / SIZE) + self.length / 2
        # triangle
        #return 2 * np.abs(i / (STREAM_LENGTH - 1) - np.floor(i / (STREAM_LENGTH - 1) + 0.5)) * SIZE
        # piece-wise 3
        f = 0.735
        if i < self.length / 3:
            return max((i / (self.length / 3) ) * f * SIZE, 1)
        elif i < 2 * self.length / 3:
            return f * SIZE
        else:
            return max((1 - (i - 2 * self.length / 3) / (self.length / 3)) * f * SIZE, 1)

    def blit(self, surface, color):
        for row in range(N_ROWS):
            sz = self.size(row)
            shape = square(sz, color)
            surface.blit(shape, ((self.col + 0.5) * SIZE - sz / 2, (row + 0.5) * SIZE - sz / 2))

N_COLS = 30
N_ROWS = 30
SIZE = 25  # pixels
DS = 0.5  # second, time sparating two streams
FPS = 20
save_screenshot = False

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

    pg.display.set_caption('HoloFace streaming animation')
    pg.mouse.set_visible(0)

    pg.display.update()  # to display the background

    clock = pg.time.Clock()  # setup clock
    t0 = pg.time.get_ticks()  # in ms
    last_t = t0
    last_s = -1
    streams = [Stream(i, 
        length=Stream.pick_length(), 
        velocity=Stream.pick_velocity()) for i in range(N_COLS)]  # inactive list of N_COLS streams

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
        #'''
        xy = np.empty((2, N_ROWS, N_COLS), dtype=int)
        rec1 = square(1, white)
        for i in range(N_ROWS):
            for j in range(N_COLS):
                xy[0, i, j] = (2 * j + 1) * (SIZE / 2)
                xy[1, i, j] = (2 * i + 1) * (SIZE / 2)
                screen.blit(rec1, (xy[0, i, j], xy[1, i, j]))
        #'''
        # update stream positions
        dt = (t - last_t) / 1000
        for stream in streams:
        	if stream.active == True:
        	    stream.position = stream.position + dt * stream.velocity  # pixels
        	    if stream.get_tail() > N_ROWS * SIZE:
        	    	# deactivate this stream
        	    	stream.position = - (stream.length - 1) / 2 * SIZE
        	    	stream.active = False
        	last_t = t
        # a new stream is activated every DS second
        ds = (t - last_s) / 1000
        if ds > DS:
            # activate a new stream
            index = np.random.randint(0, len(streams), 1)[0]
            print(streams[index])
            streams[index].active = True
            print('activating new stream at t=%.1f in col %d' % (t, streams[index].col))
            last_s = t
        for stream in streams:
            if not stream.active:
                continue
            stream.blit(screen, white)

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
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

    SIZE = 15
    STREAM_LENGTH = 31  # odd number of rows that spans a stream
    STREAM_LENGTH_STD = 10
    STREAM_VELOCITY = 110  # pixel / second
    STREAM_VELOCITY_STD = 50

    def __init__(self, col=0, length=None, velocity=None):
        self.active = False
        self.col = col
        if length == None:
            length = self.STREAM_LENGTH
        # ensure length is an odd number
        if length % 2 == 0:
            length += 1
        self.length = length
        self.position = - (self.length - 1) / 2 * Stream.SIZE
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
        return self.position + self.length / 2 * Stream.SIZE

    def get_head_row(self):
        """Compute the head row of this stream."""
        return min(self.N_ROWS, int(round(self.get_head() / Stream.SIZE)))
        
    def get_tail(self):
        return self.position - self.length / 2 * Stream.SIZE

    def get_tail_row(self):
        """Compute the tail row of this stream."""
        return max(0, int(round(self.get_tail() / Stream.SIZE)))
        
    @staticmethod
    def pick_length():
        return np.random.randint(Stream.STREAM_LENGTH - Stream.STREAM_LENGTH_STD, Stream.STREAM_LENGTH + Stream.STREAM_LENGTH_STD)

    @staticmethod
    def pick_velocity():
        return np.random.randint(Stream.STREAM_VELOCITY - Stream.STREAM_VELOCITY_STD, Stream.STREAM_VELOCITY + Stream.STREAM_VELOCITY_STD)

    def size(self, row):
        i = (row - self.position / Stream.SIZE) + self.length / 2
        # triangle
        #return 2 * np.abs(i / (STREAM_LENGTH - 1) - np.floor(i / (STREAM_LENGTH - 1) + 0.5)) * SIZE
        # piece-wise 3
        f = 0.735
        f = 0.6
        if i < self.length / 3:
            return max((i / (self.length / 3) ) * f * Stream.SIZE, 1)
        elif i < 2 * self.length / 3:
            return f * Stream.SIZE
        else:
            return max((1 - (i - 2 * self.length / 3) / (self.length / 3)) * f * Stream.SIZE, 1)

    def blit(self, surface, color, offset=0):
        # find the bounds to draw this stream
        for row in range(self.get_tail_row(), 1 + self.get_head_row()):
            sz = self.size(row)
            shape = square(sz, color)
            surface.blit(shape, (offset + (self.col + 0.5) * Stream.SIZE - sz / 2, (row + 0.5) * Stream.SIZE - sz / 2))

class Animation():

    # some default values
    DEFAULT_N_COLS = 30
    DEFAULT_N_ROWS = 30
    DEFAULT_SIZE = 15  # pixels
    DEFAULT_FPS = 10
    DEFAULT_T_s = 20  # animation period [s]
    DEFAULT_T_fade_s = 5  # fading duration [s]

    # colors
    marine = (0, 10, 50)
    white = (255, 255, 255)

    def __init__(self):
        self.bg = Animation.marine
        self.fg = Animation.white
        self.save_screenshot = False
        self.DS = 0.5  # second, time separating the activation of two streams
        self.FPS = Animation.DEFAULT_FPS
        self.SIZE = Animation.DEFAULT_SIZE
        self.T = Animation.DEFAULT_T_s * 1e3  # animation period [ms]
        self.T_fade = Animation.DEFAULT_T_fade_s * 1e3 # fading duration [ms]

        pg.init()
        # setup the screen
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        #self.screen = pg.display.set_mode((self.DEFAULT_N_COLS * self.SIZE, self.DEFAULT_N_ROWS * self.SIZE))
        display_info = pg.display.Info()
        self.height = display_info.current_h
        self.width = display_info.current_w
        print('%d x %d' % (self.width, self.height))
        self.N_COLS = min(self.width // self.SIZE, Animation.DEFAULT_N_COLS)  # keep default if enough space
        self.N_ROWS = self.height // self.SIZE
        print('%d x %d' % (self.N_ROWS, self.N_COLS))
        self.offset = (self.width - self.N_COLS * self.SIZE) / 2
        print('offset = %d' % self.offset)

        # initialize a list of N_COLS inactive streams
        self.streams = []  # empty list of streams
        for i in range(self.N_COLS):
            self.streams.append(Stream(i, length=Stream.pick_length(), velocity=Stream.pick_velocity()))
        # update the N_ROWS value for each stream
        for stream in self.streams:
            stream.N_ROWS = self.N_ROWS

        # compute the reference image
        self.ref = self.compute_ref()
        self.screen.blit(self.ref, (0, 0))

        # set up our fade surface
        self.fade = pg.Surface((self.width, self.height))
        self.fade.fill((0, 0, 0))  # black

        self.clock = pg.time.Clock()  # setup clock
        pg.display.set_caption('HoloFace streaming animation')
        pg.mouse.set_visible(0)
        pg.display.update()  # to display the background

    def blit_shape(surface, rect, color):
        """
        :param surface: Surface instance destination
        :param rect: pygame Rect instance
        :param color: color in rgb or rgba mode
        """
        rectangle = shape(rect.size[0], color)
        return surface.blit(rectangle, rect.topleft)

    def compute_ref(self):
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert()
        image.fill(self.bg)
        xy = np.empty((2, self.N_ROWS, self.N_COLS), dtype=int)
        rec1 = square(1, self.fg)
        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):
                xy[0, i, j] = (2 * j + 1) * (self.SIZE / 2)
                xy[1, i, j] = (2 * i + 1) * (self.SIZE / 2)
                image.blit(rec1, (self.offset + xy[0, i, j], xy[1, i, j]))
        return image

    def create_frame(self, t):
        #print('creating frame at time %d' % t)
        image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        image.blit(self.ref, (0, 0))
        # draw each active stream
        for stream in self.streams:
            if not stream.active:
                continue
            stream.blit(image, self.fg, offset=self.offset)
            if t > self.T:
                # start fading out the screen
                alpha = min((t - self.T) / self.T_fade * 255, 255)
                self.fade.set_alpha(alpha)
                image.blit(self.fade, (0, 0))
                if t > self.T + self.T_fade:
                    self.streaming_close = True
        return image

    def run(self):
        """Streaming animation while the program is not being used. 
        At the end of the animation, the screen fade out to full black.
        """
        self.streaming_close = False  # flag to stop the animation
        t0 = pg.time.get_ticks()  # in ms
        last_t = t0
        last_s = -1
        # main loop executing the animation
        while not self.streaming_close:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.streaming_close = True
                    break

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:  # use 'q' to quit game
                        print('exiting the game')
                        self.streaming_close = True
                        break
            t = pg.time.get_ticks()  # in ms
            # update stream positions
            dt = (t - last_t) / 1000
            for stream in self.streams:
                if stream.active == True:
                    stream.position = stream.position + dt * stream.velocity  # pixels
                    if stream.get_tail() > self.N_ROWS * self.SIZE:
                        # deactivate this stream
                        stream.position = - (stream.length - 1) / 2 * self.SIZE
                        stream.active = False
                last_t = t
            # a new stream is activated every DS second
            ds = (t - last_s) / 1000
            if ds > self.DS:
                # activate a new stream
                index = np.random.randint(0, len(self.streams), 1)[0]
                #print(self.streams[index])
                self.streams[index].active = True
                #print('activating new stream at t=%.1f in col %d' % (t, self.streams[index].col))
                last_s = t
            # compute and blit the corresponding image
            self.screen.blit(self.create_frame(t - t0), (0, 0))

            pg.display.update()
            self.clock.tick(self.FPS)

        print('thank you for playing')
        if self.save_screenshot is True:
            pg.image.save(self.screen, os.path.join('images', 'streaming.png'))
            print('screenshot was saved')
        time.sleep(0.2)
        pg.display.quit()

if __name__ == '__main__':
    anim = Animation()
    anim.run()
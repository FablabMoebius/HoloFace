# coding: utf-8
"""
Module to play the holoface animation. The animation is first calculated offline and run cyclicaly in a loop. 
The library pygame is leverage to play the animation, handle the frame rate and a few event callbacks.
"""
import sys, time, random
import pygame as pg
import os
import numpy as np
from math import sin, pi
import time
#from scipy import ndimage

class Animation():

    # some default values
    DEFAULT_N_COLS = 60
    DEFAULT_N_ROWS = 60
    DEFAULT_SIZE = 16  # pixels, even number
    DEFAULT_FPS = 5
    DEFAULT_T_s = 5  # animation period [s]
    DEFAULT_T_fade_s = 5  # fading duration [s]

    # colors
    marine = (0, 10, 50)
    white = (255, 255, 255)

    def __init__(self, fullscreen=True):
        self.bg = Animation.marine
        self.fg = Animation.white
        self.save_screenshot = False  # save the last screen image as png
        self.FPS = Animation.DEFAULT_FPS
        self.SIZE = Animation.DEFAULT_SIZE
        self.T_s = Animation.DEFAULT_T_s
        self.T = Animation.DEFAULT_T_s * 1e3  # animation period [ms]
        self.T_fade = Animation.DEFAULT_T_fade_s * 1e3 # fading duration [ms]
        self.verbose = True

        pg.init()
        display_info = pg.display.Info()
        self.height = display_info.current_h
        self.width = display_info.current_w
        # setup the screen
        if fullscreen:
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            self.SIZE = self.height // self.DEFAULT_N_ROWS
            self.N_COLS = min(self.width // self.SIZE, Animation.DEFAULT_N_COLS)  # keep default if enough space
            self.N_ROWS = self.height // self.SIZE
            self.offset = (self.width - self.N_COLS * self.SIZE) / 2
        else:
            self.screen = pg.display.set_mode((self.DEFAULT_N_COLS * self.SIZE, self.DEFAULT_N_ROWS * self.SIZE))
            self.N_COLS = Animation.DEFAULT_N_COLS
            self.N_ROWS = Animation.DEFAULT_N_ROWS
            self.offset = 0
        if self.verbose:
            print('display size: %d x %d' % (self.width, self.height))
            print('array size: %d x %d' % (self.N_ROWS, self.N_COLS))
            print('using SIZE %d' % self.SIZE)
            print('offset = %d' % self.offset)

        # compute the reference image
        self.screen.blit(self.compute_ref(), (0, 0))
        self.clock = pg.time.Clock()  # setup clock
        pg.display.set_caption('HoloFace animation')
        pg.mouse.set_visible(0)
        pg.display.update()  # to display the background

    def __getstate__(self):
        state = self.__dict__.copy()
        screen = state.pop("screen")
        state["screen_string"] = (pg.image.tostring(screen, "RGB"), screen.get_size())
        #ref = state.pop("ref")
        #state["ref"] = (pg.image.tostring(ref, "RGB"), ref.get_size())
        clock = state.pop("clock")
        return state

    def __setstate__(self, state):
        screen_string, size = state.pop("screen_string")
        state["screen"] = pg.image.fromstring(screen_string, size, "RGB")
        #ref_string, size = state.pop("ref_string")
        #state["ref"] = pg.image.fromstring(ref_string, size, "RGB")
        state["clock"] = pg.time.Clock()
        self.__dict__.update(state)

    def compute_ref(self):
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert()
        image.fill(self.bg)
        return image

def circle(size, color):
    """
    Draw a simple circle.

    :param size: the size of the circle in pixels
    :param color: color in rgb or rgba mode
    """
    shape = pg.Surface((size, size), pg.SRCALPHA)
    pg.draw.ellipse(shape, color, shape.get_rect(), 0)
    return shape

def cross(size, color):
    """
    Draw a cross shape.

    :param size: the size of the cross in pixels
    :param color: color in rgb or rgba mode
    """
    rect = pg.Rect(0, 0, size, size)
    shape = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.line(shape, color, (0, size/2), (size, size/2), max(size // 3, 1))
    pg.draw.line(shape, color, (size/2, 0), (size/2, size), max(size // 3, 1))
    return shape

def corner(size, color):
    """
    Draw a corner shape.

    :param size: the size of the corner in pixels
    :param color: color in rgb or rgba mode
    """
    rect = pg.Rect(0, 0, size, size)
    shape = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.line(shape, color, (0, size/2), (size/2, size/2), max(size // 3, 1))
    pg.draw.line(shape, color, (size/2, 0), (size/2, size/2), max(size // 3, 1))
    return shape

def square(size, color):
    """
    Draw a simple square.

    :param size: the size of the square in pixels
    :param color: color in rgb or rgba mode
    """
    rect = pg.Rect(0, 0, size, size)
    shape = pg.Surface(rect.size, pg.SRCALPHA)
    shape.fill(color)
    return shape

def rounded_square(size, color, radius=0.5):
    """
    Draw a rounded square.

    :param size: the size of the square in pixels
    :param color: color in rgb or rgba mode
    :param float radius: rounded corner ratio in [0, 1]
    """
    color = pg.Color(*color)
    alpha = color.a
    color.a = 0
    rect = pg.Rect(0, 0, size, size)
    shape = pg.Surface(rect.size, pg.SRCALPHA)

    circle = pg.Surface([min(rect.size) * 3] * 2, pg.SRCALPHA)
    pg.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pg.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = shape.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    shape.blit(circle, radius)
    radius.topright = rect.topright
    shape.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    shape.blit(circle, radius)

    shape.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    shape.fill((0, 0, 0), rect.inflate(0, -radius.h))
    shape.fill(color, special_flags=pg.BLEND_RGBA_MAX)
    shape.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MIN)
    return shape

def round_odd(x):
    """Round to nearest odd integer."""
    return (2 * (x // 2) + 1).astype(np.int)

def plot_time_functions():
    """Plot our time functions used in the animation."""
    from matplotlib import pyplot as plt
    t = np.linspace(0, 1 * T_s, 501)
    plt.figure()
    plt.plot(t, [splash_angle(1000 * tt) for tt in t], label='splash angle')
    plt.plot(t, [splash_size(1000 * tt) for tt in t], label='splash size')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.show()

def load_image(im_name):
    # read the image using pyplot
    from matplotlib import pyplot as plt
    im = plt.imread(os.path.join('images', im_name))
    if im.ndim == 3:
        im = im[:, :, 0]
    return im / im.max()  # normalize image

class HolofaceAnimation(Animation):
  
    def __init__(self, anim='random'):
        """Holoface animation.

        Different types of animations can be run depending on the variable `anim`.

        @param str anim: type of the animation, must be in ['random', 'splash', 'image']
        """
        Animation.__init__(self)
        self.anim = anim
        self.multithread = True
        self.holoface_close = False  # flag to stop the game

        # animation parameters
        #anim = 'image'  # must be in ['random', 'splash', 'image', 'wait']
        self.splash_file = 'splash_anim.npz'
        self.save_anim_png = False
        self.rot_angle = 360  # degrees, angle to rotate the target as time increases
        self.tilt_angle = 45  # degrees, angle to give a sense of depth
        
        # construct the target pattern which is used to control the sizes and the angles
        if self.anim == 'random':
            # here we use randomly distributed values for the animation
            self.target = np.random.uniform(0, 1, Animation.DEFAULT_N_COLS * Animation.DEFAULT_N_ROWS).reshape((Animation.DEFAULT_N_ROWS, Animation.DEFAULT_N_COLS))
            self.f = self.anim_size
            self.g = self.no_angle
            self.shape = rounded_square
        elif self.anim == 'splash':
            # load the logo
            im_name = 'holoface_ambigram_60x60.png'
            im_name = 'holoface_logo_57x37.png'
            self.SIZE = 15
            self.FPS = 10
            self.T_s = 5
            self.target = load_image(im_name)
            self.rot_angle = 360.
            self.tilt_angle = 0.
            self.f = self.splash_size
            self.g = self.splash_angle
            self.shape = rounded_square
        elif self.anim == 'image':
            self.target = load_image('holoface.png')
            self.rot_angle = 0.
            self.tilt_angle = 0.
            self.f = self.anim_size
            self.g = self.no_angle
            self.shape = rounded_square
        else:
            print('wrong animation type: %s' % self.anim)
            self.holoface_close = True
        # now get the actual N_ROWS, N_COLS values from the target
        self.N_ROWS, self.N_COLS = self.target.shape
        self.ONES = np.ones((self.N_ROWS, self.N_COLS), dtype=float)

        #### self.the_rec = self.shape(self.SIZE, self.fg)
        # angle should evolve between zero (low grey values) and tilt_angle (highest gray values)
        self.angles = np.zeros((self.N_ROWS, self.N_COLS), dtype=float)
        # compute the mean coordinates of each cell once and for all
        self.xy = np.empty((2, self.N_ROWS, self.N_COLS), dtype=int)
        self.rec1 = square(1, self.fg)
        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):
                self.xy[0, i, j] = (2 * j + 1) * (self.SIZE // 2)
                self.xy[1, i, j] = (2 * i + 1) * (self.SIZE // 2)
        # start with sizes equal to one everywhere
        self.sizes = self.ONES

        # this section prepare the aniation to be displayed
        if self.anim == 'splash':
            if not os.path.exists(self.splash_file):
                # save splash animation if needed
                self.all_frames = self.create_anim()
                self.all_frames.append(self.all_frames[len(self.all_frames) // 2])  # add an extra frame at the end
                anim_array = np.empty([len(self.all_frames), self.N_COLS * self.SIZE, self.N_ROWS * self.SIZE, 3], dtype=np.uint8)
                for i in range(len(self.all_frames)):
                    anim_array[i] =  self.all_frames[i]
                np.savez_compressed(self.splash_file, splash=anim_array)
                print('saving splash animation as compressed binary data')
            else:
                print('loading splash from file %s' % self.splash_file)
                anim_array = np.load(self.splash_file)['splash']
                print(anim_array.shape)
                # adjust offset
                self.offset = (self.width - anim_array.shape[1]) / 2
                print('new offset: %d' % self.offset)
                # double check the number of frames
                assert self.T_s * self.FPS <= anim_array.shape[0]

        else:
            # create the entire animation
            anim_array = self.create_anim()
        # populate the all_frame array to be displayed
        self.all_frames = [pg.pixelcopy.make_surface(anim_array[i]) for i in range(len(anim_array))]

        if self.save_anim_png:
            for i in range(len(self.all_frames)):
                pg.image.save(self.all_frames[i], 'test/%02d.png' % i)
            print('animation was saved as PNG files')
        print('done with animation')

    def __getstate__(self):
        state = self.__dict__.copy()
        screen = state.pop("screen")
        state["screen_string"] = (pg.image.tostring(screen, "RGB"), screen.get_size())
        clock = state.pop("clock")
        #the_rec = state.pop("the_rec")
        rec1 = state.pop("rec1")
        return state

    def __setstate__(self, state):
        screen_string, size = state.pop("screen_string")
        state["screen"] = pg.image.fromstring(screen_string, size, "RGB")
        state["clock"] = pg.time.Clock()
        #state["the_rec"] = self.shape(self.SIZE, self.fg)
        state["rec1"] = square(1, Animation.white)  #self.fg)
        self.__dict__.update(state)

    def blit_shape(self, surface, rect, color, angle=0):
        """
        :param surface: Surface instance destination
        :param rect: pygame Rect instance
        :param color: color in rgb or rgba mode
        :param float radius: rounded corner ratio in [0, 1]
        :param int angle: rotation angle in degrees
        """
        rectangle = self.shape(rect.size[0], color)
        r = pg.transform.rotate(rectangle, angle)
        return surface.blit(r, rect.topleft)

    def is_first_half(self, t):
        """return True if the animation is currently in the first half period, False otherwise.
        This can be used to optimize the animation speed.
        """
        return (t // (0.5 * self.T)) % 2 == 0  # True if t < 0.5 * T

    def anim_size(self, t):
        """Time function to pace the animation size."""
        return np.abs(np.sin(pi * t / self.T))

    def anim_angle(self, t):
        """Linear time function to rotate the pattern forth and back."""
        return 2 * np.abs(t / self.T - np.floor(t / self.T + 0.5))

    def no_angle(self, t):
        """This function just return zero."""
        return 0
        
    def splash_size(self, t):
        """Time function to animate the size of the splash logo."""
        return np.abs(np.sin(pi * t / self.T)) if t < 0.5 * self.T else 1

    def splash_angle(self, t):
        """Time function to animate the rotation angle of the splash logo."""
        return 2 * (t / self.T - 0.5) if t > 0.5 * self.T else 0
            
    def create_anim(self):
        anim = []
        if self.multithread:
            from multiprocessing import cpu_count
            from multiprocessing import Pool
            cores = cpu_count()  # use the maximum number of cores
            print('computing animation using %d processes...' % cores)
            num_frames_per_core = int(np.ceil(self.T_s * self.FPS / float(cores)))
            print('using %d frames per core' % num_frames_per_core)
            indices = [range(i * num_frames_per_core, min(self.T_s * self.FPS, (i + 1) * num_frames_per_core)) for i in range(cores)]
            print(indices)
            pool = Pool(processes=cores)
            results = pool.map(self.create_frames, indices)
            # here we do not check that the results are in order but it seems to work
            for result in results:
                anim.extend(result)
         
            # close the pool and wait for all processes to finish
            print('cleaning up processes')
            pool.close()
            pool.join()
            print('multiprocessing done')
            print(len(anim))
        else:
            # the animation if a list of T_s * FPS frames:
            n_frames = self.T_s * self.FPS
            anim = self.create_frames(range(n_frames))
        return anim

    def create_frames(self, indices):
        return [self.create_frame(i) for i in indices]

    def create_frame(self, i):
        print('creating frame %d' % i)
        # initialize a numpy array to dump the frame
        frame_data = np.empty([self.N_COLS * self.SIZE, self.N_ROWS * self.SIZE, 3], dtype=np.uint8)
        image = pg.Surface([self.N_COLS * self.SIZE, self.N_ROWS * self.SIZE], pg.SRCALPHA).convert()
        image.fill(self.bg)
        # compute all sizes and angles for this time increment
        t = 1000 * i / self.FPS
        rot_target = self.target #ndimage.rotate(target, rot_angle * g(t), reshape=False)
        sizes = round_odd(rot_target * 0.8 * self.SIZE * self.f(t))
        self.sizes = np.maximum(sizes, self.ONES)  # use a minimum size of 1
        angles = np.zeros_like(sizes) #rot_target * -self.tilt_angle * self.f(t)
        # draw all rectangle using list comprehension (avoid for loops for performance)
        [self.blit_shape(image, pg.Rect(self.xy[0, i, j] - self.sizes[i, j] / 2, 
                                 self.xy[1, i, j] - self.sizes[i, j] / 2, 
                                 self.sizes[i, j], self.sizes[i, j]), 
                                 self.fg, self.angles[i, j]) for j in range(self.N_COLS) for i in range(self.N_ROWS) if sizes[i, j] > 1]
        pg.pixelcopy.surface_to_array(frame_data, image, kind='P')
        return frame_data

    def run(self):
        """Run the holoface animation. """
        t0 = pg.time.get_ticks()  # in ms
        #old_blit_sequence = []

        # main loop executing the animation
        while not self.holoface_close:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.holoface_close = True
                    break

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:  # use 'q' to quit game
                        print('exiting the game')
                        self.holoface_close = True
                        break
            
            t = pg.time.get_ticks()  # in ms
            # get the corresponding image
            i = ((t - t0) / 1000 * self.FPS)
            if self.anim == 'splash' and i > self.T_s * self.FPS:
                # stay on the last frame
                i_frame = -1
            else:
                i_frame = round(i) % (self.T_s * self.FPS)
            if self.verbose:
                print('%.1f, %d' % (i, i_frame))
            self.screen.blit(self.all_frames[i_frame], (self.offset, 0))
            pg.display.update()
            self.clock.tick(self.FPS)

        print('thank you for playing')
        if self.save_screenshot is True:
            pg.image.save(self.screen, os.path.join('images', 'screenshot.png'))
            print('screenshot was saved')
        time.sleep(0.2)
        pg.display.quit()
      
if __name__ == '__main__':
    #holoface(anim='splash')
    anim = HolofaceAnimation(anim='image')
    anim.run()

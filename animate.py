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
#from scipy import ndimage

def cross(size, color):
    rect = pg.Rect(0, 0, size, size)
    rectangle = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.line(rectangle, color, (0, size/2), (size, size/2), max(size // 3, 1))
    pg.draw.line(rectangle, color, (size/2, 0), (size/2, size), max(size // 3, 1))
    return rectangle

def corner(size, color):
    rect = pg.Rect(0, 0, size, size)
    rectangle = pg.Surface(rect.size, pg.SRCALPHA)
    #pg.draw.line(rectangle, color, (-size/2, size/2), (size/2, size/2), max(size // 3, 1))
    #pg.draw.line(rectangle, color, (size/2, -size/2), (size/2, size/2), max(size // 3, 1))
    pg.draw.line(rectangle, color, (0, size/2), (size/2, size/2), max(size // 3, 1))
    pg.draw.line(rectangle, color, (size/2, 0), (size/2, size/2), max(size // 3, 1))
    return rectangle

def square(size, color):
    """
    :param size: the size of the square in pixels
    :param color: color in rgb or rgba mode
    """
    rect = pg.Rect(0, 0, size, size)
    rectangle = pg.Surface(rect.size, pg.SRCALPHA)
    rectangle.fill(color)
    return rectangle

def rounded_rect(size, color, radius=0.5):
    """
    :param size: the size of the square in pixels
    :param color: color in rgb or rgba mode
    :param float radius: rounded corner ratio in [0, 1]
    """
    color = pg.Color(*color)
    alpha = color.a
    color.a = 0
    rect = pg.Rect(0, 0, size, size)
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
    return rectangle

def blit_shape(surface, rect, color, angle=0):
    """
    :param surface: Surface instance destination
    :param rect: pygame Rect instance
    :param color: color in rgb or rgba mode
    :param float radius: rounded corner ratio in [0, 1]
    :param int angle: rotation angle in degrees
    """
    rectangle = shape(rect.size[0], color)
    r = pg.transform.rotate(rectangle, angle)
    return surface.blit(r, rect.topleft)

def round_odd(x):
    """Round to nearest odd integer."""
    return (2 * (x // 2) + 1).astype(np.int)

def is_first_half(t):
    """return True if the animation is currently in the first half period, False otherwise.
    This can be used to optimize the animation speed.
    """
    return (t // (0.5 * T)) % 2 == 0  # True if t < 0.5 * T

def anim_size(t):
    """Time function to pace the animation size."""
    return np.abs(np.sin(pi * t / T))

def anim_angle(t):
    """Linear time function to rotate the pattern forth and back."""
    return 2 * np.abs(t / T - np.floor(t / T + 0.5))

def no_angle(t):
    """This function just return zero."""
    return 0
    
def splash_size(t):
    """Time function to animate the size of the splash logo."""
    return np.abs(np.sin(pi * t / T)) if t < 0.5 * T else 1

def splash_angle(t):
    """Time function to animate the rotation angle of the splash logo."""
    return 2 * (t / T - 0.5) if t > 0.5 * T else 0

def load_image(im_name):
    # read the image using pyplot
    from matplotlib import pyplot as plt
    im = plt.imread(os.path.join('images', im_name))
    if im.ndim == 3:
        im = im[:, :, 0]
    return im / im.max()  # normalize image

def create_anim():
    anim = []
    # the animation if a list of T_s * FPS frames:
    for i in range(T_s * FPS):
        print('%.1f percent' % (100 * (i + 1) / T_s / FPS))
        anim.append(create_frame(i))
    return anim

def create_anim_multithread(cores=None):
    anim = []
    from multiprocessing import cpu_count
    from multiprocessing import Pool
    if not cores:
        cores = cpu_count()
    print('computing animation using %d processes...' % cores)
    #core_ids = list(range(0, cores))
    num_frames_per_core = int(np.ceil(T_s * FPS / float(cores)))
    print('using %d frames per core' % num_frames_per_core)
    indices = [range(i * num_frames_per_core, min(T_s * FPS, (i + 1) * num_frames_per_core)) for i in range(cores)]
    pool = Pool(processes=cores)
    results = pool.map(create_frames, indices)
    # here we do not check that the results are in order but it seems to work
    for result in results:
        anim.extend(result)
 
    # close the pool and wait for all processes to finish
    print('cleaning up processes')
    pool.close()
    pool.join()
    print('multiprocessing done')
    print(len(anim))
    return anim

def create_frames(indices):
    return [create_frame(i) for i in indices]

def create_frame(i):
    print('creating frame %d' % i)
    image = pg.Surface([N_COLS * SIZE, N_ROWS * SIZE], pg.SRCALPHA).convert()
    image.fill(marine)
    # compute all sizes and angles for this time increment
    t = 1000 * i / FPS
    rot_target = target #ndimage.rotate(target, rot_angle * g(t), reshape=False)
    sizes = round_odd(rot_target * 0.9 * SIZE * f(t))
    sizes = np.maximum(sizes, ONES)  # use a minimum size of 1
    angles = rot_target * -tilt_angle * f(t)
    # draw all rectangle using list comprehension (avoid for loops for performance)
    [blit_shape(image, pg.Rect(xy[0, i, j] - sizes[i, j] / 2, 
                             xy[1, i, j] - sizes[i, j] / 2, 
                             sizes[i, j], sizes[i, j]), 
                             white, angles[i, j]) for j in range(N_COLS) for i in range(N_ROWS) if sizes[i, j] > 1]
    frame_data = np.empty([N_COLS * SIZE, N_ROWS * SIZE, 3], dtype=np.uint8)
    pg.pixelcopy.surface_to_array(frame_data, image, kind='P')
    return frame_data

def holoface(anim='random'):
    path = os.getcwd()
    holoface_close = False  # flag to stop the game
    pg.init()
    global T_s, FPS, N_ROWS, N_COLS, SIZE, marine, target, f, T, ONES, tilt_angle, xy, white, shape
    
    # animation parameters
    #anim = 'image'  # must be in ['random', 'splash', 'image', 'wait']
    splash_file = 'splash_anim.npz'
    save_anim_png = False
    save_screenshot = False
    FPS = 10  # frame per second
    N_ROWS_DEFAULT = 35
    N_COLS_DEFAULT = 35
    SIZE = 15  # size of a square unit [pixel] - ideally take an even number
    T_s = 5 # animation period [s]
    T = T_s * 1e3 # animation period [ms]
    rot_angle = 360  # degrees, angle to rotate the target as time increases
    tilt_angle = 45  # degrees, angle to give a sense of depth

    '''
    # plot the time functions for debugging
    from matplotlib import pyplot as plt
    t = np.linspace(0, 1 * T_s, 501)
    plt.figure()
    plt.plot(t, [splash_angle(1000 * tt) for tt in t], label='splash angle')
    plt.plot(t, [splash_size(1000 * tt) for tt in t], label='splash size')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.show()
    '''

    # colors
    marine = (0, 10, 50)
    white = (255, 255, 255)

    # construct the target pattern which is used to control the sizes and the angles
    if anim == 'random':
        # here we use randomly distributed values for the animation
        target = np.random.uniform(0, 1, N_ROWS_DEFAULT * N_ROWS_DEFAULT).reshape((N_ROWS_DEFAULT, N_ROWS_DEFAULT))
        f = anim_size
        g = no_angle
        shape = rounded_rect
    elif anim == 'splash':
        # load the logo
        im_name = 'holoface_ambigram_60x60.png'
        #target = load_image('holoface_ambigram_100x38.png')
        target = load_image(im_name)
        rot_angle = 360.
        tilt_angle = 0.
        f = splash_size
        g = splash_angle
        shape = rounded_rect
    elif anim == 'image':
        target = load_image('holoface.png')
        rot_angle = 0.
        tilt_angle = 0.
        f = anim_size
        g = no_angle
        shape = rounded_rect
    elif anim == 'wait':
        # create streams going down
        n_streams = N_COLS // 6
        shape = square
    else:
        print('wrong animation type: %s' % anim)
        holoface_close = True
    # now get the actual N_ROWS, N_COLS values from the target
    N_ROWS, N_COLS = target.shape
    ONES = np.ones((N_ROWS, N_COLS), dtype=float)

    # setup the screen
    screen = pg.display.set_mode((N_COLS * SIZE, N_ROWS * SIZE))
    screen.fill(marine)

    pg.display.set_caption('HoloFace test animation')
    pg.mouse.set_visible(0)

    the_rec = shape(SIZE, white)
    # angle should evolve between zero (low grey values) and tilt_angle (highest gray values)
    angles = np.zeros((N_ROWS, N_COLS), dtype=float)
    # compute the mean coordinates of each cell once and for all
    xy = np.empty((2, N_ROWS, N_COLS), dtype=int)
    rec1 = square(1, white)
    for i in range(N_ROWS):
        for j in range(N_COLS):
            xy[0, i, j] = (2 * j + 1) * (SIZE // 2)
            xy[1, i, j] = (2 * i + 1) * (SIZE // 2)
            screen.blit(rec1, (xy[0, i, j], xy[1, i, j]))
    # start with sizes equal to one everywhere
    sizes = ONES
    old_blit_sequence = []

    # save splash animation if needed
    if anim == 'splash' and not os.path.exists(splash_file):
        all_frames = create_anim()
        all_frames.append(all_frames[len(all_frames) // 2])  # add an extra frame at the end
        splash_data = np.empty([len(all_frames), N_COLS * SIZE, N_ROWS * SIZE, 3], dtype=np.uint8)
        for i in range(len(all_frames)):
            pg.pixelcopy.surface_to_array(splash_data[i], all_frames[i], kind='P')
        np.savez_compressed(splash_file, splash=splash_data)
        print('saving splash animation as compressed binary data')
    elif anim == 'splash':
        print('loading splash from file %s' % splash_file)
        splash_data = np.load(splash_file)['splash']
        print(splash_data.shape)
        all_frames = [pg.pixelcopy.make_surface(splash_data[i]) for i in range(splash_data.shape[0])]
    else:
        # create the entire animation
        anim = create_anim_multithread()
        print(type(anim))
        print(len(anim))
        all_frames = [pg.pixelcopy.make_surface(anim[i]) for i in range(len(anim))]

    if save_anim_png:
        for i in range(len(all_frames)):
            pg.image.save(all_frames[i], 'test/%02d.png' % i)
        print('animation was saved as PNG files')
    print('done with animation')

    pg.display.update()  # to display the background

    clock = pg.time.Clock()  # setup clock
    t0 = pg.time.get_ticks()  # in ms

    # main loop executing the animation
    while not holoface_close:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                holoface_close = True
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:  # use 'q' to quit game
                    print('exiting the game')
                    holoface_close = True
                    break
        
        t = pg.time.get_ticks()  # in ms
        # get the corresponding image
        i = ((t - t0) / 1000 * FPS)
        if anim == 'splash' and i > T_s * FPS:
            i_frame = -1
        else:
            i_frame = round(i) % (T_s * FPS)
        print('%.1f, %d' % (i, i_frame))
        screen.blit(all_frames[i_frame], (0, 0))
        pg.display.update()
        clock.tick(FPS)

    print('thank you for playing')
    if save_screenshot is True:
        pg.image.save(screen, os.path.join('images', 'screenshot.png'))
        print('screenshot was saved')
    time.sleep(0.2)
    pg.display.quit()

if __name__ == '__main__':
    holoface(anim='image')

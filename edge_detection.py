# coding: utf-8
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt, cm

def detect_edges(im, debug=False):
    im8 = (im * 255).astype(np.uint8)
    print(im.shape)
    print(im.max())

    # try sobel filter
    sx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=5)
    sy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=5)
    sob = np.hypot(sx, sy).astype(np.uint8)
    print(sob.max())

    # try canny filter
    can = cv2.Canny(im8, 20, 140)  # input image must be of type CV_8U
    print(can.max())

    if debug:
        # make a 2x2 figure to display the results
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.imshow(sob, vmin=0, vmax=0.5*sob.max(), cmap=cm.gray)
        ax1.set_title('Sobel filter')
        plt.axis('off')
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.imshow(can, vmin=0, vmax=0.5*can.max(), cmap=cm.gray)
        ax2.set_title('Canny filter')
        plt.axis('off')

    def rebin(arr, new_shape):
        shape = (new_shape[0], arr.shape[0] // new_shape[0], new_shape[1], arr.shape[1] // new_shape[1])
        return arr.reshape(shape).mean(-1).mean(1)

    target_size = np.array([60, 60])
    # get the rebin factor
    k = int(im8.shape[0] / target_size[0])
    print('k = %d' % k)
    # adjust the size by cropping before the rebin
    crop_size = (np.array(sob.shape) - k * target_size) // 2

    # rebin the Sobel filtered image
    pattern = rebin(sob[crop_size[0]:crop_size[0] + k * target_size[0], 
                        crop_size[1]:crop_size[1] + k * target_size[1]], 
                        target_size)
    m = 0.5 * pattern.max()
    if debug:
        ax3 = fig.add_subplot(2, 2, 3)
        plt.imshow(pattern, interpolation='nearest', cmap=cm.gray, vmin=0., vmax=m)
        ax3.set_title('Sobel Holoface')
        plt.axis('off')

    # now with Canny
    pattern = rebin(can[crop_size[0]:crop_size[0] + k * target_size[0], 
                        crop_size[1]:crop_size[1] + k * target_size[1]], 
                        target_size)
    m = 0.5 * pattern.max()
    if debug:
        ax4 = fig.add_subplot(2, 2, 4)
        plt.imshow(pattern, interpolation='nearest', cmap=cm.gray, vmin=0., vmax=m)
        ax4.set_title('Canny Holoface')
        plt.axis('off')
        plt.imsave('images/holoface.png', pattern, cmap=cm.gray, vmin=0., vmax=m)
        plt.show()
    return pattern

if __name__ == '__main__':
    im = plt.imread('face1.png')[:, :, 0] # use 100, 200 for canny filter
    im = plt.imread('face2.png') # use , 100, 200 for canny filter
    detect_edges(im, debug=True)

# coding: utf-8
from matplotlib import pyplot as plt, cm
from scipy import ndimage
import numpy as np
import os

im = plt.imread(os.path.join('images', 'Pierre-Joseph_Proudhon.png'))[:, :, 0]
print(im.shape)

# try sobel filter
sx = ndimage.sobel(im, axis=0, mode='constant')
sy = ndimage.sobel(im, axis=1, mode='constant')
sob = np.hypot(sx, sy)
print(sob.max())

# try canny filter
from skimage.feature import canny 
can = canny(im, sigma=0.5)
print(can.max())

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax1.imshow(sob, vmin=0, vmax=0.5, cmap=cm.gray)
ax1.set_title('Sobel filter')
plt.axis('off')
ax2 = fig.add_subplot(1, 2, 2)
ax2.imshow(can, vmin=0, vmax=0.5, cmap=cm.gray)
ax2.set_title('Canny filter')
plt.axis('off')
#plt.show()

def rebin(arr, new_shape):
  shape = (new_shape[0], arr.shape[0] // new_shape[0], new_shape[1], arr.shape[1] // new_shape[1])
  return arr.reshape(shape).mean(-1).mean(1)

pattern = rebin(sob[1:571, 1:391], (57*2, 39*2))
plt.imsave('images/pj.png', pattern, cmap=cm.gray, vmax=0.4)
print(pattern.max())
plt.figure()
plt.imshow(pattern, vmin=0, vmax=0.4, interpolation='nearest', cmap=cm.gray)
plt.axis('off')
plt.show()

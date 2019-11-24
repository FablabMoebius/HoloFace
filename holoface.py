from picamera import PiCamera
import numpy as np
import os
import cv2
from face_detection import face_capture
from edge_detection import detect_edges
from animate import holoface
from matplotlib import pyplot as plt, cm

while True:
	print('new shot')
	# face detection
	face = face_capture(mode='haar', archive_face=True)
	print(face)
	if face is not None:
		# process the detected face
		pattern = detect_edges(face, debug=False)
		m = 0.5 * pattern.max()
		plt.imsave('images/holoface.png', pattern, cmap=cm.gray, vmin=0., vmax=m)
		# now run holoface if an image was taken
		holoface(anim='image')

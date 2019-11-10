from picamera import PiCamera
import numpy as np
import cv2
from edge_detection import detect_edges
from profiling import holoface

run_holoface = False

# Camera resolution height must be dividable by 16, and width by 32
cam_width = 1280  #x1944640
cam_height = 1024  #480
print ("Using camera resolution: %d x %d" % (cam_width, cam_height))
capture = np.zeros((cam_height, cam_width, 4), dtype=np.uint8)

# Initialize the camera
#camera = PiCamera(stereo_mode='side-by-side', stereo_decimate=False)
camera = PiCamera()
camera.resolution=(cam_width, cam_height)
camera.framerate = 2
camera.hflip = False

# load calibration
calib = np.load('calib.npz')
mtx = calib['mtx']
dist = calib['dist']
w = cam_width
h = cam_height
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# face detection
casc_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(casc_path)
pad = 50  # pixel to pad before saving the face

for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(cam_width, cam_height)):
	img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
	# draw the usual green rectangle around the faces
	width_list = []
	index_max = 0
	for (x, y, w, h) in faces:
		width_list.append(w)
	if len(width_list) > 0:
		index_max = np.argmax(width_list)
	for i, (x, y, w, h) in enumerate(faces):
		if i == index_max:
			color = (0, 255, 0)
		else:
			color = (0, 0, 255)
		cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
	cv2.imshow("Holoface", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop and save last image
	if key == ord('q'):
		break
	elif key == ord('h'):
		(x, y, w, h) = faces[index_max]
		# launch holoface
		face = img[y - pad:y + h + pad, x - pad:x + w + pad]
		print('saving face')
		print(img.shape)
		cv2.imwrite('face.png', face)
		detect_edges(face, debug=True)
		run_holoface = True
		break
camera.close()

# now run holoface if an image was taken
if run_holoface:
	holoface(anim='image')





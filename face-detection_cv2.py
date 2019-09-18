import cv2
import sys
from matplotlib import pyplot as plt, cm

casc_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(casc_path)
video_capture = cv2.VideoCapture(0)  # capture from the camera
pad = 20  # pixel to save the face
'''
Enter an infinite loop to capture the camera input and analyze it 
for face detection. Press the space bar to save the detected face 
or 'q' to quit.
'''
while True:
    # capture one frame
    ret, frame = video_capture.read()
    # turn image to grayscale for face detection
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

    # draw the usual green rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face detection', frame)

    key = cv2.waitKey(1)
    if len(faces) > 0 and key & 0xFF == 32:  # 32 is space bar
        # save the detected face as an image
        print('saving face')
        print(img.shape)
        print(img.max())
        plt.imsave('face.png', img[y - pad:y + h + pad, x - pad:x + w + pad], cmap=cm.gray)
    elif key & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

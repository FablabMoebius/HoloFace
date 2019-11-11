from picamera import PiCamera
import cv2
import dlib
import sys
import numpy as np
import os

face_dir = 'faces'
pad = 30  # pixel to pad before saving the face

cam_width = 640
cam_height = 480
print ("Using camera resolution: %d x %d" % (cam_width, cam_height))
capture = np.zeros((cam_height, cam_width, 4), dtype=np.uint8)

# Initialize the camera
camera = PiCamera()
camera.resolution=(cam_width, cam_height)
camera.framerate = 5
camera.hflip = False
camera.vflip = False

def face_capture(mode='haar', archive_face=True):
    """Function to capture a face.
    
    Enter an infinite loop to capture the camera input and analyze it 
    for face detection. Press the space bar to save the detected face 
    or 'q' to quit.
    
    :param str mode: should be 'haar' or 'landmark
    :param bool archive_face: a flag to archive detected face to the faces folder
    """
    face = None
    assert mode in ['haar', 'landmark']
    if mode == 'haar':
        casc_path = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(casc_path)
    elif mode == 'landmark':
        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)

    # capture live frames from the camera and analyze them
    for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(cam_width, cam_height)):
        # turn image to grayscale for face detection
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if mode == 'haar':
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
            # draw the usual green rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif mode == 'landmark':
            faces = detector(img, 1)
            print("Number of faces detected: {}".format(len(faces)))
            for bb in faces:
                x, y, w, h = bb.left(), bb.top(), bb.width() + 1, bb.height() + 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # get the landmarks for each face
                shape = predictor(img, bb)
                points = [(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)]
                for p in points:
                    cv2.circle(frame, (p[0], p[1]), 1, (0, 0, 255), -1)            
        # Display the resulting frame
        cv2.imshow('Face detection', frame)

        key = cv2.waitKey(1)
        if len(faces) > 0 and key & 0xFF == 32:  # 32 is space bar
            face = img[y - pad:y + h + pad, x - pad:x + w + pad]
            if archive_face:
                # save the face in the faces folder
                l = os.listdir(face_dir)
                l.sort()
                last_face_index = int(l[-1][4:8])
                face_path = os.path.join(face_dir, 'face%04d.png' % (1 + last_face_index))
                cv2.imwrite(face_path, face)
            break
        elif key & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return face
    
if __name__ == '__main__':
    #face_capture(mode='haar')
    face_capture(mode='landmark')

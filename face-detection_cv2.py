import cv2
import dlib
import sys
from matplotlib import pyplot as plt, cm

casc_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(casc_path)
video_capture = cv2.VideoCapture(0)  # capture from the camera
pad = 30  # pixel to pad before saving the face

def face_capture(save_face=True):
    '''Function to capture a face.
    
    Enter an infinite loop to capture the camera input and analyze it 
    for face detection. Press the space bar to save the detected face 
    or 'q' to quit.
    '''
    face = None
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
            face = img[y - pad:y + h + pad, x - pad:x + w + pad]
            # save the detected face as an image
            print('saving face')
            print(img.shape)
            print(img.max())
            plt.imsave('face.png', face, cmap=cm.gray)
            break
        elif key & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
    return face

def face_landmark():
    predictor_path = 'shape_predictor_68_face_landmarks.dat.bz2'
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    img = dlib.load_rgb_image('faces/face0001.png')
    faces = detector(img, 1)
    print("Number of faces detected: {}".format(len(faces)))
    
if __name__ == '__main__':
    #face_capture()
    face_landmark()

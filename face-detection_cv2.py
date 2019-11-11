import cv2
import dlib
import sys
from matplotlib import pyplot as plt, cm

casc_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(casc_path)
video_capture = cv2.VideoCapture(0)  # capture from the camera
pad = 30  # pixel to pad before saving the face

FACIAL_LANDMARKS_68_IDXS = dict([
	("mouth", (48, 68)),
	("inner_mouth", (60, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 36)),
	("jaw", (0, 17))
])

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
    predictor_path = 'shape_predictor_68_face_landmarks.dat'
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    img = dlib.load_rgb_image('faces/face0001.png')

    faces = detector(img, 1)
    print("Number of faces detected: {}".format(len(faces)))
    for k, d in enumerate(faces):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))
        points = [(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)]
        print(shape.num_parts)
        for i, (x, y) in enumerate(points):
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

    # Display the resulting frame
    cv2.imshow('Face landmarks detection', img)
    cv2.imwrite('face_landmarks.png', img)
    key = cv2.waitKey(1000)
    cv2.destroyAllWindows()
    """
    while True:
        # capture one frame
        ret, frame = video_capture.read()
        # turn image to grayscale for face detection
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(img, 1)
        print("Number of faces detected: {}".format(len(faces)))

        for k, d in enumerate(faces):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))

        # Display the resulting frame
        cv2.imshow('Face landmarks detection', frame)

        key = cv2.waitKey(1)
        if len(faces) > 0 and key & 0xFF == 32:  # 32 is space bar
            #face = img[y - pad:y + h + pad, x - pad:x + w + pad]
            ## save the detected face as an image
            #print('saving face')
            #print(img.shape)
            #print(img.max())
            #plt.imsave('face.png', face, cmap=cm.gray)
            break
        elif key & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
    return face
    """
    
if __name__ == '__main__':
    #face_capture()
    face_landmark()

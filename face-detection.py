# coding: utf-8
'''
[En] Test face detection
[Fr] Test de détection des visages
'''

from SimpleCV import Camera, Display
from time import sleep

myCamera = Camera(prop_set={'width':720, 'height': 1280})
myDisplay = Display(resolution=(720, 1280))

while not myDisplay.isDone():
    frame = myCamera.getImage()
    faces = frame.findHaarFeatures('face.xml')
    if faces:
        for face in faces:
            print("Face at: " + str(face.coordinates()))
    else:
        print("No faces detected.")
    frame.save(myDisplay)
    sleep(.1)

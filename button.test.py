# Test of the push buttons
from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Blue button gpio 23 / pin 16
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Yellow button gpio 24 / pin 18
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for button to be pressed !")

while True:
    if GPIO.input(16) == False:
        print("Blue button Pushed")
        sleep(1)
        
    if GPIO.input(18) == False:
        print("Yellow button Pushed")
        sleep(1)

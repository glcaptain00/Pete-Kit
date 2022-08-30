############################################
# Task 1: Perform initial setup of devices #
############################################
import cv2
import RPi.GPIO as gpio
from datetime import datetime
from time import sleep

#Configuration
pin_button = 16

#Setup camera
cam = cv2.VideoCapture(0)

#Setup GPIO
gpio.setmode(gpio.BOARD) # Use the board numbering
gpio.setup(pin_button, gpio.IN)

###############################################
# Task 2: create a function to take a picture #
###############################################
def capture(channel):
    print("Capturing image...")
    ret, image = cam.read() #ret is true if the frame was read correctly, false otherwise. image is the frame itself.
    filename = datetime.now().strftime("%m-%d-%YT%H-%M-%S.png") #Get a string representation of the date and time to store as a file
    cv2.imwrite(f'./{filename}', image)
    print("Done!")

################################################
# Task 3: Assign an action to the button press #
################################################
gpio.add_event_detect(pin_button, gpio.RISING, callback=capture)

##################################################
# Creating an infinite loop to keep the program  #
# alive while waiting on the button press        #
##################################################
while True:
    cam.grab() #Read through frames to clear them from the buffer
    sleep(0.1)
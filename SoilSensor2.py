#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO SETUP
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water Detected!")
    else:
        print("No Water Detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

try:
    # infinite loop
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted by user. Exiting...")
finally:
    GPIO.cleanup() 

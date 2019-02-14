import sys, os
import RPi.GPIO as GPIO


def setupLED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)


def greenLED(switch):
    GPIO.output(21, switch)


def redLED(switch):
    GPIO.output(20, switch)


def rgbLED(switch):
    GPIO.output(5, switch[0])
    GPIO.output(6, switch[1])
    GPIO.output(12, switch[2])
    GPIO.output(13, switch[3])

def cleanUp():
    print("LEDs are clean")
    GPIO.cleanup()

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

### Instructions for the rasperry
"""import RPi.GPIO as GPIO
import time

GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)"""

class Ironcar():
    """Class of the car. Contains all the different fields, functions needed to
    control the car.
    """

    def __init__(self):

        self.mode = 'resting'  # resting, training, auto or dirauto
        self.started = False  # If True, car will move, if False car won't move.
        self.model = None
        self.direction = 3#1=hard left 2=left 3=straigth 4=right 5=hard right

        self.verbose = True # Verbose is a general programming term for produce lots of logging output.

        # Camera Attribut
        self.streaming_state = False
        self.n_img = 0
"""
        # PWM setup
        try:
            from Adafruit_PCA9685 import PCA9685

            self.pwm = PCA9685()
            self.pwm.set_pwm_freq(60)
        except Exception as e:
            print('The car will not be able to move')
            print('Are you executing this code on your laptop?')
            print('The adafruit error: ', e)
            self.pwm = None

        self.load_config()

        from threading import Thread

        self.camera_thread = Thread(target=self.camera_loop, args=())
        self.camera_thread.start()

    def gas(self, value): # puissance/vitesse de la voiture
        #Sends the pwm signal on the gas channel

        if self.pwm is not None:
            self.pwm.set_pwm(self.commands['gas_pin'], 0, value)
            if self.verbose:
                print('GAS : ', value)
        else:
            if self.verbose:
                print('GAS : ', value)

    def dir(self, value):
        #Sends the pwm signal on the dir channel

        if self.pwm is not None:
            self.pwm.set_pwm(self.commands['dir_pin'], 0, value) # (channel ,on time start, value)
            if self.verbose:
                print('DIR : ', value)
        else:
            if self.verbose:
                #print('PWM module not loaded')
                print('DIR : ', value)

    def default_call(self, img, prediction):
        Default function call. Does nothing.

        pass
    """
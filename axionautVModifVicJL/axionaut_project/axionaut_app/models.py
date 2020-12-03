from django.db import models
import numpy as np
import os
import json
CAM_RESOLUTION = (250, 150)
from PIL.Image import fromarray as PIL_convert
#from utils import ConfigException, CameraException
get_default_graph = None  # For lazy imports




CONFIG = './config.json'

# Create your models here.

# Instructions for the rasperry
"""import RPi.GPIO as GPIO
import time

GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)mode

GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)"""


class Ironcar():
    """Class of the car. Contains all the different fields, functions needed to
    control the car.
    """

    def __init__(self):

        self.graph = None # voir predict_from_img A QUOI CA SERT ?
        self.mode = 'resting'  # resting, training, auto or dirauto
        # If True, car will move, if False car won't move.
        self.started = False
        self.model_loaded=False
        self.model = None
        self.direction = 3  # 1=hard left 2=left 3=straigth 4=right 5=hard right
        # Verbose is a general programming term for produce lots of logging output.
        self.verbose = True
        self.mode_function = self.default_call

        # Camera Attribut
        self.streaming_state = False
        self.n_img = 0


        from threading import Thread

        self.camera_thread = Thread(target=self.camera_loop, args=())
        self.camera_thread.start()

        """
        # PWM setup
        try:
            from Adafruit_PCA9685 import PCA9685

            self.pwm = PCA9685()
            self.pwm.set_pwm_freq(60)
        except Exception as e:
            print('The car ill not be able to move')
            print('Are you executing this code on your laptop?')
            print('The adafruit error: ', e)
            self.pwm = None

        self.load_config()

        

    def gas(self, value):  # puissance/vitesse de la voiture
        # Sends the pwm signal on the gas channel

        if self.pwm is not None:
            self.pwm.set_pwm(self.commands['gas_pin'], 0, value)
            if self.verbose:
                print('GAS : ', value)
        else:
            if self.verbose:
                print('GAS : ', value)

    def dir(self, value):
        # Sends the pwm signal on the dir channel

        if self.pwm is not None:
            # (channel ,on time start, value)
            self.pwm.set_pwm(self.commands['dir_pin'], 0, value)
            if self.verbose:
                print('DIR : ', value)
        else:
            if self.verbose:
                # print('PWM module not loaded')
                print('DIR : ', value)

        """

    def default_call(self, img, prediction):
        # Default function call. Does nothing.
        pass

    def load_config(self):
        #if not os.path.isfile(CONFIG):
            #raise ConfigException('The config file `{}` does not exist'.format(CONFIG))

        with open(CONFIG) as json_file:
            config = json.load(json_file)

        # Verify that the config file has the good fields
            error_message = '{} is not present in the config file'
        #for field in ['commands', 'fps', 'datasets_path', 'stream_path', 'models_path']:
            #if field not in config:
                #raise ConfigException(error_message.format(field))

        #for field in ["dir_pin", "gas_pin", "left", "straight", "right", "stop","neutral", "drive", "drive_max", "invert_dir"]:
            #if field not in config['commands']:
                #raise ConfigException(error_message.format('[commands][{}]'.format(field)))

        self.commands = config['commands']
        self.fps = config['fps']

        # Folder to save the stream in training to create a dataset
        # Only used in training mode
        from datetime import datetime

        ct = datetime.now().strftime('%Y_%m_%d_%H_%M')
        self.save_folder = os.path.join(config['datasets_path'], str(ct))
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        # Folder used to save the stream when the stream is on
        self.stream_path = config['stream_path']
        if not os.path.exists(self.stream_path):
            os.makedirs(self.stream_path)

        return config


    def camera_loop(self):
            """Makes the camera take pictures and save them.
            This loop is executed in a separate thread.
            """

            from io import BytesIO
            from base64 import b64encode

            try:
                from picamera import PiCamera
                from picamera.array import PiRGBArray
            except Exception as e:
                print('picamera import error : ', e)

            try:
                cam = PiCamera(framerate=self.fps)
            except Exception as e:
                print('Exception ', e,'yoooooooooooooo')
                #raise CameraException()

            image_name = os.path.join(self.stream_path, 'capture.jpg')

            cam.resolution = CAM_RESOLUTION
            cam_output = PiRGBArray(cam, size=CAM_RESOLUTION)
            stream = cam.capture_continuous(cam_output, format="rgb", use_video_port=True)

            for f in stream:
                img_arr = f.array
                im = PIL_convert(img_arr)
                im.save(image_name)

                # Predict the direction only when needed
                if self.mode in ['dirauto', 'auto'] and self.started:
                    prediction = self.predict_from_img(img_arr)
                else:
                    prediction = [0, 0, 1, 0, 0]
                self.mode_function(img_arr, prediction)

                if self.streaming_state:
                    index_class = prediction.index(max(prediction))

                    buffered = BytesIO()
                    im.save(buffered, format="JPEG")
                    img_str = b64encode(buffered.getvalue())
                    #socketio.emit('picture_stream', {'image': True, 'buffer': img_str.decode(
                        #'ascii'), 'index': index_class, 'pred': [float(x) for x in prediction]}, namespace='/car')

                cam_output.truncate(0)

    def predict_from_img(self, img):
        """Given the 250x150 image from the Pi Camera.
        Returns the direction predicted by the model (array[5])
        """
        try:
            img = np.array([img[20:, :, :]])

            with self.graph.as_default():
                pred = self.model.predict(img)
                if self.verbose:
                    print('pred : ', pred)
            pred = list(pred[0])
        except Exception as e:
            # Don't print if the model is not relevant given the mode
            if self.verbose and self.mode in ['dirauto', 'auto']:
                print('Prediction error : ', e)
            pred = [0, 0, 1, 0, 0]

        return pred
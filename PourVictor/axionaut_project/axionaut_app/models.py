import time
from PIL.Image import fromarray as PIL_convert
from django.db import models
import numpy as np
import os
import json
CAM_RESOLUTION = (250, 130)
#from utils import ConfigException, CameraException
get_default_graph = None  # For lazy imports


CONFIG = './config.json'

# Create your models here.

# Instructions for the rasperry
#import RPi.GPIO as GPIO

# GPIO Mode (BOARD / BCM)
# GPIO.setmode(GPIO.BCM)


class Ironcar():
    """Class of the car. Contains all the different fields, functions needed to
    control the car.
    """

    def __init__(self):

        self.graph = None  # voir predict_from_img A QUOI CA SERT ?
        self.mode = 'resting'  # resting, training, auto or dirauto
        # if True, car will move, if False car won't move.
        self.started = False
        self.model_loaded = False
        self.model = None
        self.current_model = None
        self.curr_dir = 0
        self.curr_gas = 0
        self.max_speed_rate = 0.8
        self.speed_mode = 'constant'
        # Verbose is a general programming term for produce lots of logging output.
        self.verbose = False
        self.mode_function = self.default_call
        self.dir_on_value = 0  # Valeur du dir a afficher sur l'interface
        self.gas_on_value = 0  # Valeur du gas a afficher sur l'interface
        self.status = "Stop"

        # Camera Attribut
        #self.streaming_state = False
        self.n_img = 0

        from threading import Thread

        # self.camera_thread = Thread(target=self.camera_loop, args=()) DECOMMENTER
        # self.camera_thread.start() DECOMMENTER

        self.load_config()

        # PWM setup
        # try:
        #    from Adafruit_PCA9685 import PCA9685

        #    self.pwm = PCA9685()
        #    self.pwm.set_pwm_freq(60)
        # except Exception as e:
        #    print('The car ill not be able to move')
        #    print('Are you executing this code on your laptop?')
        #    print('The adafruit error: ', e)
        #    self.pwm = None

    def gas(self, value):  # puissance/vitesse de la voiture
        # Sends the pwm signal on the gas channel

        if self.pwm is not None:
            self.pwm.set_pwm(self.commands['gas_pin'], 0, value)
            if self.verbose:
                print('(SERVER) GAS: ', value)
        else:
            if self.verbose:
                print('(SERVER) GAS: ', value)

    def dir(self, value):
        # Sends the pwm signal on the dir channel

        if self.pwm is not None:
            # (channel ,on time start, value)
            self.pwm.set_pwm(self.commands['dir_pin'], 0, value)
            if self.verbose:
                print('(SERVER) DIR: ', value)
        else:
            if self.verbose:
                # print('PWM module not loaded')
                print('(SERVER) DIR: ', value)

    def default_call(self, img, prediction):
        # Default function call. Does nothing.
        pass

    def load_config(self):
        # if not os.path.isfile(CONFIG):
        #raise ConfigException('The config file `{}` does not exist'.format(CONFIG))

        with open(CONFIG) as json_file:
            config = json.load(json_file)

        # Verify that the config file has the good fields
            error_message = '{} is not present in the config file'

        # for field in ['commands', 'fps', 'datasets_path', 'stream_path', 'models_path']:
            # if field not in config:
            #raise ConfigException(error_message.format(field))

        # for field in ["dir_pin", "gas_pin", "left", "straight", "right", "stop","neutral", "drive", "drive_max", "invert_dir"]:
            # if field not in config['commands']:
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
        # print(self.stream_path)
        # Folder used to save the stream when the stream is on
        # print(config['stream_path'])
        self.stream_path = config['stream_path']
        if not os.path.exists(self.stream_path):
            os.makedirs(self.stream_path)

        return config

    def save_image(self, folder):  # used when we select the folder where image will be saved
        with open(CONFIG) as json_file:
            config = json.load(json_file)
        # Folder to save the stream in training to create a dataset
        # Only used in training mode
        from datetime import datetime

        ct = datetime.now().strftime('%Y_%m_%d_%H_%M')
        self.save_folder = os.path.join(
            config['datasets_path'], str(ct), folder)
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        # print(self.stream_path)
        # Folder used to save the stream when the stream is on
        # print(config['stream_path'])
        self.stream_path = config['stream_path']
        if not os.path.exists(self.stream_path):
            os.makedirs(self.stream_path)

    def predict_from_img(self, img):
        """Given the 250x150 image from the Pi Camera.
        Returns the direction predicted by the model (array[5])
        """
        try:
            #img = np.array([img[20:, :, :]])
            # with self.graph.as_default():
            pred = self.model.predict(img)
            # if self.verbose:
            #print('pred : ', pred)
            pred = np.argmax(list(pred[0]))  # [0, 1, 2, 3, 4]
            #pred = list(pred[0])
        except Exception as e:
            # Don't print if the model is not relevant given the mode
            if self.verbose and self.mode in ['dirauto', 'auto']:
                print('Prediction error : ', e)
            print("Exception")
            pred = [0, 0, 1, 0, 0]

        return pred

    def pred_direction(self, prediction):
        '''
        Transforme un chiffre en mot.       
        '''
        directions = ["hard left", "left", "straight", "right", "hard right"]

        return directions[prediction]

    def autopilot(self, img, prediction):
        """Sends the pwm gas and dir values according to the prediction of the
        Neural Network (NN).

        img: unused. But has to stay because other modes need it.
        prediction: array of softmax
        """

        #print("(SERVER) CURRENT_MODEL: ", self.current_model)
        if self.started:

            print("(SERVER) PREDICTION: ", self.pred_direction(prediction))
            coeffs = [0.45, 0.7, 1., 0.7, 0.45]
            speed_mode_coef = coeffs[prediction]
            #print('speed_mode_coef: {}'.format(speed_mode_coef))

            # On inverse pour que les signeaux coïncide bien avec les directions des roues
            local_dir = -(-1 + 2 * float(prediction)/float(4))
            local_gas = self.max_speed_rate * speed_mode_coef

            gas_value = int(
                local_gas * (self.commands['drive_max'] - self.commands['drive']) + self.commands['drive'])
            dir_value = int(
                local_dir * (self.commands['right'] - self.commands['left'])/2. + self.commands['straight'])
            self.dir_on_value = dir_value
            self.gas_on_value = gas_value
            #print("(SERVER) self.started: True")

            self.gas(gas_value)
            self.dir(dir_value)

        else:
            gas_value = self.commands['neutral']
            dir_value = self.commands['straight']
            #print("(Server) self.started: False")
            self.gas(gas_value)
            self.dir(dir_value)

    def training(self, img):
        """
        Enregistre les images du stream lorsque started = True.
        """

        image_name = '_'.join(['frame', str(self.n_img), 'gas',
                               str(self.curr_gas), 'dir', str(self.curr_dir)])
        image_name += '.jpg'
        image_name = os.path.join(self.save_folder, image_name)

        img_arr = np.array(img[20:, :, :], copy=True)
        img_arr = PIL_convert(img_arr)
        img_arr.save(image_name)

        self.n_img += 1

    def on_gas(self, data):
        """Triggered when a value from the keyboard/gamepad is received for gas.

        data: intensity of the key pressed.
        """

        if not self.started:
            return

        # Ignore gas commands if not in training/dirauto mode
        if self.mode not in ['training', 'dirauto']:
            if self.verbose:
                print('Ignoring gas command')
            return

        self.curr_gas = float(data) * self.max_speed_rate

        if self.curr_gas < 0:
            new_value = self.commands['stop']
        elif self.curr_gas == 0:
            new_value = self.commands['neutral']
        else:
            new_value = int(
                self.curr_gas * (self.commands['drive_max']-self.commands['drive']) + self.commands['drive'])
        self.gas(new_value)

    def on_dir(self, data):
        """Triggered when a value from the keyboard/gamepad is received for dir.

        data: intensity of the key pressed.
        """

        if not self.started:
            return

        # Ignore dir commands if not in training mode
        if self.mode not in ['training']:
            if self.verbose:
                print('Ignoring dir command')
            return

        self.curr_dir = self.commands['invert_dir'] * float(data)
        if self.curr_dir == 0:
            new_value = self.commands['straight']
        else:
            new_value = int(
                self.curr_dir * (self.commands['right'] - self.commands['left'])/2. + self.commands['straight'])
        self.dir(new_value)

    def max_speed_update(self, new_max_speed):
        """Changes the max_speed of the car."""

        self.max_speed_rate = new_max_speed
        if self.verbose:
            print('The new max_speed is : ', self.max_speed_rate)
        return self.max_speed_rate

    def switch_speed_mode(self, speed_mode):
        """Changes the speed mode of the car"""

        self.speed_mode = speed_mode
        msg = 'Speed mode set to {}'.format(speed_mode)

    def select_model(self, model_name):
        # Changes the model of autopilot selected and loads it.
        model_name = './models/'+model_name
        data = {'type': 'info',
                'msg': 'Loading model {}...'.format(model_name)}
        print(data)

        if model_name == self.current_model:
            data = {'type': 'info', 'msg': 'Model {} already loaded.'.format(
                self.current_model)}
            print(data)
            return

        try:
            # Only import tensorflow if needed (it's heavy)
            global get_default_graph  # Qu'est-ce que c'est que global?
            if get_default_graph is None:
                try:
                    import tensorflow
                    #import autokeras as ak
                    from keras.models import load_model
                    print("(SERVER) importation of the packages")
                except Exception as e:
                    msg = 'Error while importing ML librairies. Got error {}'.format(
                        e)
                    data = {'type': 'danger', 'msg': msg}
                    print(data)

                    if self.verbose:
                        print('ML error : ', e)
                    return

            if self.verbose:
                print('Selected model: ', model_name)

            self.model = load_model(
                model_name, custom_objects=ak.CUSTOM_OBJECTS)
            self.current_model = model_name
            self.model_loaded = True
            self.switch_mode(self.mode)

            data = {'type': 'success', 'msg': 'The model {} has been successfully loaded'.format(
                self.current_model)}
            print(data)
            print("(SERVER) CURRENT_MODEL: ", self.current_model)

            if self.verbose:
                print('The model {} has been successfully loaded'.format(
                    self.current_model))

        except Exception as e:
            data = {'type': 'danger', 'msg': 'Error while loading model {}. Got error {}'.format(
                model_name, e)}
            print(data)

            if self.verbose:
                print('An Exception occured : ', e)

    def switch_mode(self, new_mode):
        """Switches the mode between:
                - training
                - resting
                - dirauto
                - auto
        """

        # always switch the starter to stopped when switching mode
        self.started = False

        # Stop the gas before switching mode and reset wheel angle (safe)
        # self.gas(self.commands['neutral']) DECOMMENTER
        # self.dir(self.commands['straight']) DECOMMENTER

        if new_mode == "auto":
            self.mode = 'auto'
            if self.model_loaded:
                self.mode_function = self.autopilot
            else:
                if self.verbose:
                    print("(SERVER) model not loaded")
        elif new_mode == "training":
            self.mode = 'training'
            #self.mode_function = self.training
        else:
            self.mode = 'resting'
            self.mode_function = self.default_call

        # Make sure we stopped and reset wheel angle even if the previous mode
        # sent a last command before switching.
        # self.gas(self.commands['neutral']) DECOMMENTER
        # self.dir(self.commands['straight']) DECOMMENTER

        if self.verbose:
            print('(SERVER) switched to mode: ', new_mode)

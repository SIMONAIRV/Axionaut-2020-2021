from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse

from .models import Ironcar

from axionaut_app.camera import Camera

import json
import os
from .forms import ModelsForm
from PIL import Image
import io
import numpy as np
from datetime import datetime

car = Ironcar()

CONFIG = './config.json'
with open(CONFIG) as json_file:
    config = json.load(json_file)
    MODELS_PATH = config['models_path']


def gen_training(camera):

    while True:
        frame = camera.get_frame()
        img = np.array(Image.open(io.BytesIO(frame)))
        if car.started == True:
            car.training(img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_training(request):

    return StreamingHttpResponse(gen_training(Camera()), content_type="multipart/x-mixed-replace; boundary=frame")


def gen_auto(camera):

    while True:
        frame = camera.get_frame()
        img = np.array(Image.open(io.BytesIO(frame)))
        img = np.expand_dims(img, axis=0)
        if car.model is not None:
            pred = car.predict_from_img(img)
            car.autopilot(img, pred)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_auto(request):

    return StreamingHttpResponse(gen_auto(Camera()), content_type="multipart/x-mixed-replace; boundary=frame")


def commandes(request):
    car.switch_mode("training")

    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode,
        "status": car.status

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def auto(request):

    if car.started == False:
        started = True
        car.status = "Start"
    else:
        started = False
        car.status = "Stop"
    car.started = started
    # getting list of models
    models = []
    if os.path.isdir(MODELS_PATH):
        # models_name = [os.path.join(MODELS_PATH, f) for f in os.listdir(
        #     MODELS_PATH) if f.endswith('.hdf5')]
        models_name = [f for f in os.listdir(MODELS_PATH)]

    # switching mode
    models = ModelsForm()
    car.switch_mode("auto")

    # loading model
    if request.GET:
        temp = request.GET['models']
        model_name = models_name[int(temp)]
        print('SERVER : models : ', model_name)
        car.select_model(model_name)
        if car.model_loaded:
            car.mode_function = car.autopilot
        else:
            if car.verbose:
                print("model not loaded")
        print("(SERVER) after loading started: ", car.started)

   

    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode,
        "form": models,
        "status": car.status
    }
    return render(request, 'axionaut_app/auto.html', {"car": myCar})


def menu(request):
    return render(request, 'axionaut_app/menu.html', {})


def dir_neutral(request):
    car.direction = 3
    car.on_dir(0)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def dir_left(request):
    car.direction = 2
    car.on_dir(-1)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def dir_right(request):
    car.direction = 4
    car.on_dir(1)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def gas_neutral(request):
    car.on_gas(0)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def gas_forward(request):
    car.on_gas(1)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def gas_backward(request):
    car.on_gas(-1)
    myCar = {
        "speed_mode": car.speed_mode,
        "model": car.current_model,
        "gas": car.curr_gas,
        "dir": car.curr_dir,
        "mode": car.mode

    }
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})


def start_stop(request):
    
    if car.started == False:
        started = True
        car.status = "Start"
    else:
        started = False
        car.status = "Stop"

    car.started = started

    

    # Stop the gas before switching mode and reset wheel angle (safe)
    car.gas(car.commands['neutral']) # pwm setup DECOMMENTER
    car.dir(car.commands['straight']) # pwm setup DECOMMENTER
    myCar = {
    "speed_mode": car.speed_mode,
    "model": car.current_model,
    "gas": car.gas_on_value,
    "dir": car.dir_on_value,
    "mode": car.mode,
    "status": car.status

    }
   
    return render(request, 'axionaut_app/commandes.html', {"car": myCar})

def start_stop_auto(request):

     
    if car.started == False:
        started = True
        car.status = "Start"
    else:
        started = False
        car.status = "Stop"

    car.started = started
    print("(SERVER) car.started = ", car.started)


    # Stop the gas before switching mode and reset wheel angle (safe)
    car.gas(car.commands['neutral']) # pwm setup DECOMMENTER
    car.dir(car.commands['straight']) # pwm setup DECOMMENTER
    models = ModelsForm()

    myCar = {
    "speed_mode": car.speed_mode,
    "model": car.current_model,
    "gas": car.gas_on_value,
    "dir": car.dir_on_value,
    "mode": car.mode,
    "form": models,
    "status": car.status
    }
    return render(request, 'axionaut_app/auto2.html', {"car": myCar})

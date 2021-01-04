from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse

from .models import Ironcar

from .camera import Camera

import json
import os

car = Ironcar()

CONFIG = './config.json'
with open(CONFIG) as json_file:
    config = json.load(json_file)
    MODELS_PATH = config['models_path']

def gen(camera):

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video(request):

    return StreamingHttpResponse(gen(Camera()), content_type="multipart/x-mixed-replace; boundary=frame")


def commandes(request):
    car.mode="training"
    
    return render(request, 'axionaut_app/commandes.html', {})

def auto(request):
    #switching mode 
    
    car.mode="auto"
    #loading model
    """
    if car.model_loaded:
        car.mode_function = car.autopilot
    else:
        if car.verbose:
            #socketio.emit('msg2user', {'type': 'warning','msg': 'Model not loaded'}, namespace='/car')
            print("model not loaded")"""

    models = []
    print(os.path.isdir(MODELS_PATH))
    if os.path.isdir(MODELS_PATH):
        #models = [os.path.join(MODELS_PATH, f) for f in os.listdir(MODELS_PATH) if f.endswith('.hdf5')]
        models = [os.path.join(MODELS_PATH, f) for f in os.listdir(MODELS_PATH)]
        
    print('SERVER : models : ', models)
    context ={
        'models' : models
    }
    return render(request, 'axionaut_app/auto.html', context)

def menu(request):
    return render(request, 'axionaut_app/menu.html', {})

def dir_neutral(request):
    car.direction=3
    print('direction : ')
    print(car.direction)
    car.on_dir(0)
    return render(request, 'axionaut_app/commandes.html', {})

def dir_left(request):
    car.direction=2
    print('direction : ')
    print(car.direction)
    car.on_dir(-1)
    return render(request, 'axionaut_app/commandes.html', {})

def dir_right(request):
    car.direction=4
    print('direction : ')
    print(car.direction) 
    car.on_dir(1)   
    return render(request, 'axionaut_app/commandes.html', {})

def gas_neutral(request):
    print('gas : 0')
    car.on_gas(0)
    return render(request, 'axionaut_app/commandes.html', {})

def gas_forward(request):
    print('gas : 1')
    car.on_gas(1)
    return render(request, 'axionaut_app/commandes.html', {})

def gas_backward(request):
    print('gas : -1')
    car.on_gas(-1)
    return render(request, 'axionaut_app/commandes.html', {})


def start_stop(request):

    if car.started==True :
        started=False
    else:
        started=False

    car.started=started
    
    # Stop the gas before switching mode and reset wheel angle (safe)
    car.gas(car.commands['neutral']) #pwm setup
    car.dir(car.commands['straight']) #pwm setup

    return render(request, 'axionaut_app/commandes.html', {})


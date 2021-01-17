from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse

from .models import Ironcar

# from axionaut_app.camera import Camera DECOMMENTER

import json
import os
from .forms import ModelsForm

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
    car.switch_mode("training")
    return render(request, 'axionaut_app/commandes.html', {})


def auto(request):
    # getting list of models
    models = []
    if os.path.isdir(MODELS_PATH):
        # models_name = [os.path.join(MODELS_PATH, f) for f in os.listdir(
        #     MODELS_PATH) if f.endswith('.hdf5')]
        models_name = [f for f in os.listdir(MODELS_PATH)]

    # switching mode
    context = {}
    models = ModelsForm()
    car.switch_mode("auto")

    # loading model
    if request.GET:
        temp = request.GET['Models']
        model_name = models_name[int(temp)]
        print('SERVER : models : ', model_name)
        car.select_model(model_name)
        if car.model_loaded:
            car.mode_function = car.autopilot
        else:
            if car.verbose:
                print("model not loaded")

    context['form'] = models

    return render(request, 'axionaut_app/auto.html', context)


def menu(request):
    return render(request, 'axionaut_app/menu.html', {})


def dir_neutral(request):
    car.direction = 3
    print('direction : ', car.direction)
    car.on_dir(0)
    return render(request, 'axionaut_app/commandes.html', {})


def dir_left(request):
    car.direction = 2
    print('direction : ', car.direction)
    car.on_dir(-1)
    return render(request, 'axionaut_app/commandes.html', {})


def dir_right(request):
    car.direction = 4
    print('direction : ', car.direction)
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

    if car.started == True:
        started = False
    else:
        started = False

    car.started = started

    # Stop the gas before switching mode and reset wheel angle (safe)
    # car.gas(car.commands['neutral'])  # pwm setup DECOMMENTER
    # car.dir(car.commands['straight'])  # pwm setup DECOMMENTER

    return render(request, 'axionaut_app/commandes.html', {})


def start_stop_auto(request):
    if car.started == True:
        started = False
    else:
        started = False

    car.started = started

    # Stop the gas before switching mode and reset wheel angle (safe)
    # car.gas(car.commands['neutral'])  # pwm setup DECOMMENTER
    # car.dir(car.commands['straight'])  # pwm setup DECOMMENTER

    return render(request, 'axionaut_app/auto.html', {})

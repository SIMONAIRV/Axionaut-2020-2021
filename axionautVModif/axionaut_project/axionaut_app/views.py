from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Ironcar

car = Ironcar()

def commandes(request):
    return render(request, 'axionaut_app/commandes.html', {})

def auto(request):
    return render(request, 'axionaut_app/auto.html', {})

def menu(request):
    return render(request, 'axionaut_app/menu.html', {})

def update_up(request):
    car.direction=3
    print('direction : ')
    print(car.direction)
    return render(request, 'axionaut_app/commandes.html', {})

def update_left(request):
    car.direction=2
    print('direction : ')
    print(car.direction)
    return render(request, 'axionaut_app/commandes.html', {})

def update_right(request):
    car.direction=4
    print('direction : ')
    print(car.direction)    
    return render(request, 'axionaut_app/commandes.html', {})

def update_down(request):
    car.direction=0
    print('direction : ')
    print(car.direction)    
    return render(request, 'axionaut_app/commandes.html', {})
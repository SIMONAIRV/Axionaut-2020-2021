from django.shortcuts import render

from django.http import HttpResponse

from .models import Car

# Create your views here.
car = Car(name="Axionaut", up=0, left=0, upLeft=0, upRight=0, right=0, down=0, mode="X")

def commandes(request):
    return render(request, 'axionaut_app/commandes.html', {})

def menu(request):
    return render(request, 'axionaut_app/menu.html', {})

def update_up(request):
	car.up = 1
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 0
	car.mode = "Up"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	#return HttpResponse()
	return render(request, 'axionaut_app/maj.html', context)

def update_left(request):
	car.up = 0
	car.left = 1
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 0
	car.mode = "Left"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)

def update_right(request):
	car.up = 0
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 1
	car.down = 0
	car.mode = "Right"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)

def update_down(request):
	car.up = 0
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 1
	car.mode = "Down"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)


def update_up2(request):
	car.up = 1
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 0
	car.mode = "Up"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)

def update_left2(request):
	car.up = 0
	car.left = 1
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 0
	car.mode = "Left"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)

def update_right2(request):
	car.up = 0
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 1
	car.down = 0
	car.mode = "Right"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)

def update_down2(request):
	car.up = 0
	car.left = 0
	car.upLeft = 0
	car.upRight = 0
	car.right = 0
	car.down = 1
	car.mode = "Down"
	context = {
		'car_mode': car.mode,
		'car_up': car.up,
		'car_left': car.left,
		'car_upLeft': car.upLeft,
		'car_upRight': car.upRight,
		'car_right': car.right,
		'car_down': car.down,
	}
	return render(request, 'axionaut_app/maj.html', context)
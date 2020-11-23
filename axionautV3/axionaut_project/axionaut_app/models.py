from django.db import models

# Create your models here.

class Ironcar():
    """Class of the car. Contains all the different fields, functions needed to
    control the car.
    """

    def __init__(self):

        self.mode = 'resting'  # resting, training, auto or dirauto
        self.started = False  # If True, car will move, if False car won't move.
        self.model = None
        self.direction = 3#1=hard left 2=left 3=straigth 4=right 5=hard right
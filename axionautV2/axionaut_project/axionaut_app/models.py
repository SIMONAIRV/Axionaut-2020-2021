from django.db import models

# Create your models here.

class Car(models.Model):
	name = models.CharField(max_length=200)
	up = models.IntegerField(null=True)
	left = models.IntegerField(null=True)
	upLeft = models.IntegerField(null=True)
	upRight = models.IntegerField(null=True)
	right = models.IntegerField(null=True)
	down = models.IntegerField(null=True)
	mode = models.CharField(max_length=200)

	def __str__(self):
		return self.name
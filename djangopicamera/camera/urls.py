from django.urls import path, include
from camera import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video', views.video, name="video"),
]

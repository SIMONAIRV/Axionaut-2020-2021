from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    url(r'^dir_neutral/$', views.dir_neutral, name="dir_neutral"),
    url(r'^dir_right/$', views.dir_right, name="dir_right"),
    url(r'^dir_left/$', views.dir_left, name="dir_left"),
    url(r'^gas_neutral/$', views.gas_neutral, name="gas_neutral"),
    url(r'^gas_backward/$', views.gas_backward, name="gas_backward"),
    url(r'^gas_forward/$', views.gas_forward, name="gas_forward"),
    url(r'^video_training/$', views.video_training, name="video_training"),
    url(r'^video_auto/$', views.video_auto, name="video_auto"),
    url(r'^start_stop_auto/$', views.start_stop_auto, name='start_stop_auto'),

]

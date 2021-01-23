from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # url(r'^update_up/$', views.update_up, name="update_up"),
    # url(r'^update_left/$', views.update_left, name="update_left"),
    # url(r'^update_right/$', views.update_right, name="update_right"),
    # url(r'^update_down/$', views.update_down, name="update_down"),
    url(r'^dir_neutral/$', views.dir_neutral, name="dir_neutral"),
    url(r'^dir_right/$', views.dir_right, name="dir_right"),
    url(r'^dir_left/$', views.dir_left, name="dir_left"),
    url(r'^gas_neutral/$', views.gas_neutral, name="gas_neutral"),
    url(r'^gas_backward/$', views.gas_backward, name="gas_backward"),
    url(r'^gas_forward/$', views.gas_forward, name="gas_forward"),
    url(r'^video', views.video, name="video"),
]

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    url(r'^update_up/$', views.update_up, name="update_up"),
    url(r'^update_left/$', views.update_left, name="update_left"),
    url(r'^update_right/$', views.update_right, name="update_right"),
    url(r'^update_down/$', views.update_down, name="update_down"),
    url(r'^update_up2/$', views.update_up2, name="update_up2"),
    url(r'^update_left2/$', views.update_left2, name="update_left2"),
    url(r'^update_right2/$', views.update_right2, name="update_right2"),
    url(r'^update_down2/$', views.update_down2, name="update_down2"),
]

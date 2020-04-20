from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'init', views.init),
    path(r'getDevices', views.getDevices),
    path(r'createPiDevice/<int:deviceId>', views.createPiDevice),
    path(r'getPiDevices', views.getPiDevices),
    path(r'getPiDevicePins/<int:piDeviceId>', views.getPiDevicePin),
    path(r'attachPiDevicePinToBoard/<int:piDevicePinId>', views.attachPiDevicePinToBoard),
    path(r'unAttachPiDevicePinToBoard/<int:piDevicePinId>', views.unAttachPiDevicePinToBoard),
    path(r'led/<int:piDeviceId>/<str:switch>', views.led),
    path(r'start', views.start),
]
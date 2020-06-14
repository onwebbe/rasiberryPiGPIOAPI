from django.contrib import admin
from django.urls import path, include
from . import views
from . import DevicesView
urlpatterns = [
    path(r'init', views.init),
    path(r'getDevices', views.getDevices),
    path(r'createPiDevice/<int:deviceId>', views.createPiDevice),
    path(r'getPiDevices', views.getPiDevices),
    path(r'getPiDeviceById/<int:piDeviceId>', views.getPiDeviceById),
    path(r'getPiDevicesByDeviceId/<int:deviceId>', views.getPiDevicesByDeviceId),
    path(r'updatePiDevice/<int:piDeviceId>', views.updatePiDevice),
    path(r'deletePiDevice/<int:piDeviceId>', views.deletePiDeviceById),

    path(r'getPiDevicePins/<int:piDeviceId>', views.getPiDevicePin),
    path(r'attachPiDevicePinToBoard/<int:piDevicePinId>', views.attachPiDevicePinToBoard),
    path(r'unAttachPiDevicePinToBoard/<int:piDevicePinId>', views.unAttachPiDevicePinToBoard),
    path(r'led/<int:piDeviceId>/<str:switch>', views.led),
    path(r'DHT22/<int:piDeviceId>', DevicesView.getDHT22Data),
    path(r'BMP180/<int:piDeviceId>', DevicesView.getBMP180Data),
    path(r'GY30/<int:piDeviceId>', DevicesView.getGY30Data),
    path(r'RainDrop/<int:piDeviceId>', DevicesView.getRainDropData),
    path(r'RotationCount/<int:piDeviceId>', DevicesView.getRotationCountData),
    path(r'start', views.start),
]
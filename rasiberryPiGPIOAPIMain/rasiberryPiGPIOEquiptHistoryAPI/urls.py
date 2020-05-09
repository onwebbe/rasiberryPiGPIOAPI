from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'getDeviceDataHistory/<int:piDeviceId>', views.getHistoryData),
    path(r'getTodaySingleGraphData/<int:piDeviceId>/<str:deviceDataName>', views.getTodaySingleGraphData)
    
]
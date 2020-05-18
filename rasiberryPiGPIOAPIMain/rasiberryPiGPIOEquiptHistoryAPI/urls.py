from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'getDeviceDataHistory/<int:piDeviceId>', views.getHistoryData),
    path(r'getTodaySingleGraphData/<int:piDeviceId>/<str:deviceDataName>', views.getTodaySingleGraphData),
    path(r'getHistoryChartList', views.getHistoryChartList),
    path(r'addHistoryChartList', views.addHistoryChart),
    path(r'updateHistoryChartList/<int:chartId>', views.updateHistoryChart),
    path(r'deleteHistoryChart/<int:chartId>', views.deleteHistoryChart),
    path(r'getDeviceDataNamesByDeviceId/<int:piDeviceId>', views.getDeviceDataNamesByDeviceId),
]
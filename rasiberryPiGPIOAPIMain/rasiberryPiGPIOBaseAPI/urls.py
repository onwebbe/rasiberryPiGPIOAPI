from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'overview/', views.gpio_overview),
    path(r'setPinStatus/', views.gpio_setPinStatus)
]
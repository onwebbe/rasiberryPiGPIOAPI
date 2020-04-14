from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'overview/', views.gpio_overview),
    path(r'setPinStatus/<int:boardID>/<int:level>', views.gpio_setPinStatus),
    path(r'getPinStatus/<int:boardID>', views.gpio_getPinStatus),
    path(r'PWNStart/<int:boardID>', views.gpio_pwn_start),
    path(r'PWNChangeDutyCycle/<int:boardID>/<int:cycle>', views.gpio_pwn_change_duty_cycle),
    path(r'PWNChangeDutyCycle/<int:boardID>/<int:frequency>', views.gpio_pwn_change_frequency),
    path(r'PWNStop/<int:boardID>', views.gpio_pwn_stop),
]
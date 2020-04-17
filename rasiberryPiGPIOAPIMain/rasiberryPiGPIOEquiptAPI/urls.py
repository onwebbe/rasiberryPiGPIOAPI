from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path(r'LED/<str:name>/<int:boardID>/<int:GNDBoardId>/<str:switch>/', views.led)
]
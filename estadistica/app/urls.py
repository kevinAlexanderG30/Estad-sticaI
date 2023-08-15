from django.contrib import admin
from django.urls import path, include
from . import views
from .views import DatosExcel
from .views import guia2

urlpatterns = [
     path("", views.index, name="index"),
    path('guia2/', guia2, name= 'guia2'),
     path('Datos/', DatosExcel.as_view(), name='Excel-Datos'),
]


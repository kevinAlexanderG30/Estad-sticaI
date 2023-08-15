from django.contrib import admin
from django.urls import path, include
from . import views
from .views import DatosExcel,  FrecuenciaExcel

urlpatterns = [
     path("", views.index, name="index"),
     path('Datos/', DatosExcel.as_view(), name='Excel-Datos'),
     path('frecuencia/', FrecuenciaExcel.as_view(), name='Frecuencia'),
]


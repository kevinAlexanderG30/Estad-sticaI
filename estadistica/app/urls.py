from django.contrib import admin
from django.urls import path, include
from . import views
from .views import DatosExcel, FrecuenciaExcel
from .views import guia2

urlpatterns = [
     path("", views.index, name="index"),
     path("principal/", views.IndexView, name="principal"),
     path('guia2/', guia2, name= "guia2"),

     path('frecuencia/', FrecuenciaExcel.as_view(), name='Frecuencia'),
]


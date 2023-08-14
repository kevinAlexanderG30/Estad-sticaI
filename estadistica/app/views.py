# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import math

def index(request):
    return render(request, "index.html")

# Api
class DatosExcel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        content = {
            'status': 'request was permitted'
        } 
        datos = request.data
        flattened_data = [float(item) for sublist in datos for item in sublist]
        print(flattened_data)

        # Numero de datos
        N_datos = len(flattened_data)

        # Numero Mayor
        N_mayor = max(flattened_data)

        # Numero Menor
        N_menor = min(flattened_data)

        # Rango
        rango = N_mayor - N_menor

        # N° deinterva
        N_intervalos = 1+3.322 * math.log10(N_datos)

        # Amplitud
        Amplitud = rango/N_intervalos


        return Response([N_datos,  N_mayor, N_menor
                         , rango, N_intervalos, Amplitud], status=status.HTTP_201_CREATED)
    


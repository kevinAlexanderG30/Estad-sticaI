# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from statistics import mean, median, mode, variance, stdev
from numpy import percentile, array, repeat
import math
import numpy as np

N_datos = 0
arreglo = []

def index(request):
    return render(request, "index.html")

def guia2(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data') 
        numbers = [int(num) for num in input_data.split(',')]

        if numbers:
            mean_value = mean(numbers)
            median_value = median(numbers)
            try:
                mode_value = mode(numbers)
            except:
                mode_value = None
            variance_value = variance(numbers)
            stdev_value = stdev(numbers)
            q1 = percentile(numbers, 25)
            q3 = percentile(numbers, 75)
            coef_of_var = (stdev_value / mean_value) * 100

            grouped_data = {}
            for num in numbers:
                if num in grouped_data:
                    grouped_data[num] += 1
                else:
                    grouped_data[num] = 1

            freq_list = []
            value_list = []
            for value, freq in grouped_data.items():
                freq_list.append(freq)
                value_list.append(value)

            freq_array = array(freq_list)
            value_array = array(value_list)
            mean_grouped = sum(freq_array * value_array) / sum(freq_array)
            variance_grouped = sum(freq_array * (value_array - mean_grouped)**2) / sum(freq_array)
        else:
            mean_value = None
            median_value = None
            mode_value = None
            variance_value = None
            stdev_value = None
            q1 = None
            q3 = None
            coef_of_var = None
            mean_grouped = None
            variance_grouped = None

        mean_valueR = round(mean_value)
        median_valueR = round(median_value)
        mode_valueR = round(mode_value)
        variance_valueR = round(variance_value)
        stdev_valueR = round(stdev_value)
        q1R = round(q1)
        q3R = round(q3)
        coef_of_varR = round(coef_of_var)
        mean_groupedR = round(mean_grouped)
        variance_groupedR = round(variance_grouped)

        # Devuelve una respuesta JSON en lugar de renderizar directamente        
        response_data = {
            "mean": mean_value,
            "median_value": median_value,
            "mode_value": mode_value,
            "variance_value": variance_value,
            "stdev_value": stdev_value,
            "q1": q1,
            "q3": q3,
            "coef_of_var": coef_of_var,
            "mean_grouped": mean_grouped,
            "variance_grouped": variance_grouped,            
            "meanR": mean_valueR,
            "median_valueR": median_valueR,
            "mode_valueR": mode_valueR,
            "variance_valueR": variance_valueR,
            "stdev_valueR": stdev_valueR,
            "q1R": q1R,
            "q3R": q3R,
            "coef_of_varR": coef_of_varR,
            "mean_groupedR": mean_groupedR,
            "variance_groupedR": variance_groupedR,            
        }

        return JsonResponse(response_data)

   
    return render(request, "guia2.html")


# Api
class FrecuenciaExcel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        datos_float = [[float(item) for item in sublist] for sublist in arreglo[0]]


        datos1 = []
        datos = request.data
        for i in datos:
            datos1.append(float(i))
        
     
        # Calcular la frecuencia
        frecuencia = np.histogram(datos_float, bins=datos)[0]
        frecuencia1 = -(N_datos - len(frecuencia))
        frecuenciat = np.insert(frecuencia, 0, frecuencia1)
        total = sum(frecuenciat)
        return Response({"frecuenciatotal": frecuenciat, "total": total},status=status.HTTP_201_CREATED)


class DatosExcel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        content = {
            'status': 'request was permitted'
        } 
        datos = request.data

        flattened_data = [float(item) for sublist in datos for item in sublist]
        arreglo.append(datos)
        # Numero de datos
        N_datos = len(flattened_data)
        print(N_datos)

        # Numero Mayor
        N_mayor = max(flattened_data)

        # Numero Menor
        N_menor = min(flattened_data)

        # Rango
        rango = round(N_mayor - N_menor,2)
        rango_rendondeado = math.ceil(N_mayor - N_menor)

        # N° deinterva
        N_intervalos = 1+3.322 * math.log10(N_datos)
        N_redondeado =   math.ceil(N_intervalos)
       # print(f"{rango_rendondeado} /{N_redondeado}")
        # Amplitud
        Amplitud = rango_rendondeado/N_redondeado
        #print(Amplitud)
      
        return Response([N_datos,  N_mayor, N_menor
                         , rango, N_intervalos, Amplitud], status=status.HTTP_201_CREATED)
    


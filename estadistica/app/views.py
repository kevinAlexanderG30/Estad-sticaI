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

arreglo = []

def index(request):
    return render(request, "index.html")

def guia2(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data') 
        numbers = [int(num) for num in input_data.split(',')]

        # Calcula la media, mediana, moda, varianza, desviación estándar, cuartiles y coeficiente de variación
        if numbers:
            mean_value = mean(numbers)
            median_value = median(numbers)
            try:
                mode_value = mode(numbers)
            except:
                mode_value = None  # Manejo si no hay una moda clara
            variance_value = variance(numbers)
            stdev_value = stdev(numbers)
            q1 = percentile(numbers, 25)  # Primer cuartil (Q1)
            q3 = percentile(numbers, 75)  # Tercer cuartil (Q3)
            coef_of_var = (stdev_value / mean_value) * 100  # Coeficiente de variación

            # Calcula la media y la varianza de datos agrupados
            grouped_data = {}  # Diccionario para almacenar frecuencias por grupo
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

        print(numbers)
        print("Media muestral:", mean_value)
        print("Mediana muestral:", median_value)
        print("Moda muestral:", mode_value)
        print("Varianza muestral:", variance_value)
        print("Desviación estándar muestral:", stdev_value)
        print("Primer cuartil (Q1):", q1)
        print("Tercer cuartil (Q3):", q3)
        print("Coeficiente de variación:", coef_of_var)
        print("Media de datos agrupados:", mean_grouped)
        print("Varianza de datos agrupados:", variance_grouped)

        return render(request, "guia2.html", {
            "mean": mean_value,
            "median_value": median_value,
            "mode_value": mode_value,
            "variance_value": variance_value,
            "stdev_value": stdev_value,
            "q1": q1,
            "q3": q3,
            "coef_of_var": coef_of_var,
            "mean_grouped": mean_grouped,
            "variance_grouped": variance_grouped
        })
    return render(request, "guia2.html")





# Api
class FrecuenciaExcel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        datos1 = []
        datos = request.data
        print(datos)
        for i in datos:
            datos1.append(float(i))

        # Calcular la frecuencia
        frecuencia = np.histogram(arreglo, bins=datos1)[0]
        print(frecuencia)
        
        return Response("A",status=status.HTTP_201_CREATED)


class DatosExcel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        content = {
            'status': 'request was permitted'
        } 
        datos = request.data
        flattened_data = [float(item) for sublist in datos for item in sublist]
        print(flattened_data)
        arreglo.append(flattened_data)
        # Numero de datos
        N_datos = len(flattened_data)

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
        print(f"{rango_rendondeado} /{N_redondeado}")
        # Amplitud
        Amplitud = rango_rendondeado/N_redondeado
        print(Amplitud)
      
        return Response([N_datos,  N_mayor, N_menor
                         , rango, N_intervalos, Amplitud], status=status.HTTP_201_CREATED)
    


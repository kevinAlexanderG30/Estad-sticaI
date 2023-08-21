# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from statistics import mean, median, mode, variance, stdev
from numpy import percentile, array, repeat
from math import floor, ceil, log10
import pandas as pd
import numpy as np

N_datos = 0
arreglo = []

def principal(request):
    return render(request, "principal.html")


def index(request):
    return render(request, "principal.html")

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

# Funcion para contar numeros en un rango (Frecuencia absoluta)

def freqabs(lista, linferior, lsuperior):
    # Filtrar elementos en la lista que coincidan en los intervalos Y contarlos
    return len([x for x in lista if x >= linferior and x <= lsuperior])

# Funcion para acumular freq absolutas

def freqabsacum(lista):
    acumulado = 0
    # Recorriendo la lista de freq absolutas
    for i in lista:
        # Sumando la freq anterior
        acumulado = acumulado + i
    # Retornando el valor 
    return acumulado


def freqrel(lista,total): #Funcion que calcula la frecuencia relativa / frecuencia relativa acumulada

    for i in lista:#Recorriendo la lista de freq absolutas / absoluta acumulada
        freqactual = i / total #Calculando la frecuencia relativa
    # Retornando el valor
    return freqactual

def freqpor(lista): #Funcion para calcular la freq porcentual / freq porcentual acumulada

    for i in lista: #Recorriendo la lista de freq relativas / freq relativa acumulada
        freqactual = i * 100 #Calculando la frecuencia porcentual
    # Retornando el valor
    return freqactual


def IndexView(request):
    if request.method == 'POST':
        input_data = request.POST["tabla_datos"]
        
        if not input_data:
            return Response({'message': 'No hay datos'}, status=status.HTTP_400_BAD_REQUEST)
        
        table = pd.DataFrame(columns=[ #Se crea un dataframe(estructura bidimensional) para asignar los datos
            'Numero',
            'Clase',
            'Marcasdeclase',
            'Frecuenciaabsoluta',
            'Frecuenciaabsolutaacumulada',
            'Frecuenciarelativa',
            'Frecuenciarelativaacumulada',
        ])

        #Asignamos las listas, estas estaran al inicio del POST para limpiar sus datos cada refresco de pagina
        data = [] #Este contendrá los datos proporcionados por el usuario
        fabs  = [] #Frecuencia absoluta
        fabsacum  = [] #Frecuencia absoluta acumulada
        frel = [] #Frecuencia relativa
        frelacum = [] #Frecuencia relativa acumulada
        marcas = [] #marcas de clase


        data = [float(value) for value in input_data.split()]

        #Formulas utilizadas
        Total = len(data) #Este toma el total de datos que hay en la lista
        MaxValue = max(data) #Obtiene el dato mas alto
        MinValue = min(data) #Obtiene el dato mas bajo
        r =  max(data)-min(data) #Rango
        linferior = floor(MinValue) #Redondear al entero mas cercano para tomar el limite inferior
        intervalos = 1 + (3.322 * log10(Total)) #Formula para sacar los intervalos
        k = round(intervalos) #Redondeamos el dato
        lon = r / k #Longitud o amplitud
        
        #Formulas de la guia2
        mean = np.mean(data) #media aritmetica
        median = np.median(data) #mediana
        variance = np.var(data, ddof=1)  #Usar ddof=1 para calcular la varianza muestral
        std_deviation = np.std(data, ddof=1)  #Usar ddof=1 para calcular la desviación estándar muestral

        q1 = np.percentile(data, 25) #primer cuartil
        q3 = np.percentile(data, 75) #tercer cuartil
        interquartile_range = q3 - q1
        #data.sort()  # Ordenar en forma creciente
        sorted_data = sorted(data)  #Obtener una nueva lista ordenada
        
        for i in range(1, round(intervalos)+1): #Ciclo que recorre los intervalos

            lsuperior = ceil(linferior + lon) #Calculando el limite superior y redondeandolo a su próximo más cercano
            marcas.append((linferior + lsuperior) / 2) #Añadiendo a la lista las marcas de clase
            fabs.append(freqabs (data, linferior, lsuperior)) #Añadiendo a la lista las frecuencias absolutas 
            fabsacum.append(freqabsacum(fabs)) #Añadiendo a la lista Las frecuencias absolutas acumuladas
            frel.append(freqrel(fabs,Total)) #Añadiendo a la lista Las frecuencias relativas 
            frelacum.append(freqrel(fabsacum,Total)) #Añadiendo a la lista las frecuencias relativas acumuladas

            table.loc[i] = [i,f"[{linferior}, {lsuperior})", (linferior + lsuperior) / 2, freqabs(data, linferior, lsuperior), freqabsacum(fabs), freqrel(fabs,Total), freqrel(fabsacum,Total)] #Añadiendole valores a la tabla

            linferior = lsuperior#Modificando en valor del límite inferior en cada iteración


        #Se divivio en dos para mejor orden
        data_dict = {
            "Media Aritmética": mean,
            "Mediana": median,
            "Varianza Muestral": variance,
            "Desviación Estándar Muestral": std_deviation,
            "Primer Cuartil": q1,
            "Tercer Cuartil": q3,
            "Rango Intercuartil": interquartile_range,
        }

        data_dict2 = {
            "Total de datos": Total,
            "Valor mínimo": min(data),
            "Valor máximo": max(data),
            "Rango": r,
        }      

        context = {
            'table': table,
            'list': data_dict,
            'list2': data_dict2,
            'sort_list': sorted_data,
        }
        print(context)
        
        return render(request, "tablas.html", context)
    return render(request, "principal.html")



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
        rango_rendondeado = ceil(N_mayor - N_menor)

        # N° deinterva
        N_intervalos = 1+3.322 * log10(N_datos)
        N_redondeado =   ceil(N_intervalos)
       # print(f"{rango_rendondeado} /{N_redondeado}")
        # Amplitud
        Amplitud = rango_rendondeado/N_redondeado
        #print(Amplitud)
      
        return Response([N_datos,  N_mayor, N_menor
                         , rango, N_intervalos, Amplitud], status=status.HTTP_201_CREATED)
    


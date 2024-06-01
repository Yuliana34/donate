from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def conectar_frontend(request):
    data = {'mensaje': '¡conexión exitosa con el backend!'}
    return JsonResponse(data)

def index(request):
    return render(request, 'administrador/index.html')

def donado(request):
    return render(request, 'administrador/donado.html')

    
def donar_boton(request):
    return render(request, 'administrador/formdonar.html')

def causas(request):
    return render(request, 'administrador/causes.html')


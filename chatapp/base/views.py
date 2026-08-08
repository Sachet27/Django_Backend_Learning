from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def newroom(request):
    return render(request, 'newroom.html')
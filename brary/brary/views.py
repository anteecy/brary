from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    context = dict()
    return render(request, 'brary/home.html', context)

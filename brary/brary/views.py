from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def home(request):
    context = dict()
    return render(request, 'brary/home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
        context = {"form": form}
        return render(request, 'brary/registration.html', context)

@login_required
def profile(request):
    context = {"user": request.user}
    return render(request, 'brary/profile.html', context)

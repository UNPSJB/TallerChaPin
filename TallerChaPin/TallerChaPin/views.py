from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .forms import TallerAuthenticationForm


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html', {"title": "Hola Mundo"})


def login(request):
    return render(request, 'login.html', {"title": "Hola Mundo", "form": TallerAuthenticationForm()})


def logout(request):
    django_logout(request)
    return redirect('/login')

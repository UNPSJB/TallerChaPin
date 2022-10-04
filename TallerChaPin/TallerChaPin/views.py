from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from .forms import TallerAuthenticationForm


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html', {"title": "Hola Mundo"})


def login(request):
    no_user = False
    form = TallerAuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return redirect(reverse_lazy('home'))
        else:
            # TODO: revisar. Añado el flag porque en este caso user es None en el server 
            # pero AnonymousUser en el template y no puedo mostrar los msjs de error en el template.
            no_user = True 
    return render(request, 'login.html', {  
        "title": "TallerChaPin | Iniciar sesión", 
        "form": TallerAuthenticationForm(), 
        "no_user": no_user
    })


def logout(request):
    django_logout(request)
    return redirect('/login')


def template_taller(request):
    return render(request, 'template_taller_home.html', {"title": "Gestion de Taller", "ayuda": "home.html#taller"})

def template_ordenes(request):
    return render(request, 'template_ordenes_home.html', {"title": "Gestion de Ordenes", "ayuda": "home.html#presupuestos"})

def template_facturas(request):
    return render(request, 'template_facturas_home.html', {"title": "Gestion de Facturas", "ayuda": "home.html#facturas"})

def template_listados(request):
    return render(request, 'template_listados_home.html', {"title": "Visualización de listados", "ayuda": "home.html#listados"})
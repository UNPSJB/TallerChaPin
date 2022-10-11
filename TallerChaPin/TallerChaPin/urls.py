"""TallerChaPin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from TallerChaPin.views import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('taller/', include('taller.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('facturas/', include('facturas.urls')),
    path('taller/', template_taller, name='taller_home'),
    path('ordenes/', template_ordenes, name='ordenes_home'),
    path('facturas/', template_facturas, name='facturas_home'),
    path('listados/', template_listados, name='listados_home'),
    path('admin/', admin.site.urls),
    re_path(r'^docs/', include('docs.urls')),
]

handler404 = Error404View.as_view()


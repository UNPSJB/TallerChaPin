from django.urls import path

from .views import index, listado_marcas, modelos_x_marcas


urlpatterns = [
    path('', index),
    path('marcas/', listado_marcas),
    path('marcas/<slug:marca>/modelos', modelos_x_marcas, name="modelosXmarcas")
]

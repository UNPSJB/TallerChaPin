from django.urls import path

from .views import (
    index, 
    listado_marcas, 
    modelos_x_marcas, 
    registrar_cliente, 
    MarcaListView, 
    ModeloListView
)


urlpatterns = [
    path('', index),
    path('marcas/', listado_marcas),
    path('marcas/<slug:marca>/modelos', modelos_x_marcas, name="modelosXmarcas"),
    path('cliente/registrar', registrar_cliente, name="registrarCliente"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos")
]

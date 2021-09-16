from django.urls import path

from .views import (
    ClienteListView,
    index, 
    listado_marcas, 
    modelos_x_marcas, 
    registrar_cliente, 
    MarcaListView, 
    ModeloListView,
    MarcaCreateView,
    ClienteListView
)


urlpatterns = [
    path('', index),
    path('marcas/', listado_marcas),
    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),
    path('marcas/<slug:marca>/modelos', modelos_x_marcas, name="modelosXmarcas"),
    path('cliente/registrar', registrar_cliente, name="registrarCliente"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    path('clientes/listar', ClienteListView.as_view(), name='listarClientes')
]

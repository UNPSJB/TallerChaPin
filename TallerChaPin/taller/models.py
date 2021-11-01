from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
# http://....../?atributo__contains=valor
# FILTRO = {'atributo__contains': valor}
# ...?nombre__icontains=a&marca__exact=1

def validacion_nombre_unico(modelo,campo,value):
    aux= dict([(f"{campo}__iregex",f'^{value}$')])
    if modelo.objects.filter(**aux).exists():
       raise ValidationError({"nombre": "nombre ya existe"})
   # return validateeven
            


def texto_to_query(texto):
    filtros = dict([chunk.split("=") for chunk in texto.split("&")])
    filtro = models.Q()
    for attr, value in filtros.items():
        if value.isdigit():
            value = int(value)
        filtro &= models.Q(**{attr: value})
    return filtro


class MarcaQuerySet(models.QuerySet):
    def filtrar(self, texto):
        return self.filter(texto_to_query(texto))


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    objects = MarcaQuerySet.as_manager()

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(Marca,"nombre",self.nombre)
        return super().clean()

class ModeloQuerySet(models.QuerySet):
    def filtrar(self, texto):
        return self.filter(texto_to_query(texto))


class Modelo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    marca = models.ForeignKey(
        Marca, related_name="modelos", on_delete=models.CASCADE)
    anio = models.PositiveSmallIntegerField()

    # Manager de la clase Modelo
    objects = ModeloQuerySet.as_manager()

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(Modelo,"nombre",self.nombre)
        return super().clean()

class TipoTarea(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    # Requiere Material[si/no]
    materiales = models.BooleanField(default=False)
    # Requiere Repuesto[si/no]
    repuestos = models.BooleanField(default=False)
    # Requiere Planilla[si/no]
    planilla = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(TipoTarea,"nombre",self.nombre)
        return super().clean()

class Tarea(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class TipoRepuesto(models.Model):
    # Ejemplos: Puesta Derecha, Puerta Izquierda, Guardabarros, Parabrisa.
    # nombre
    # descripcion
    pass


class Repuesto(models.Model):
    TIPOS = (
        (1, 'Puerta'),
        (2, 'Guardabarros'),
        (3, 'Parabrisa'),
        (4, 'Cristal'),
        (5, 'Bateria'),
        (6, 'Rueda'),
        (7, 'Mecanico'),
        (8, 'Llanta'),
        (9, 'Suspension'),
        (10, 'Aire Acondicionado'),
        (99, 'Otro'),
    )
    nombre = models.CharField(max_length=50)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    
    def __str__(self):
        return self.nombre


class TipoMaterial(models.Model):
    GRAMO = 1
    CM3 = 2
    LITRO = 3
    UNIDAD = 4
    KG = 5
    METRO = 6
    METRO2 = 7
    UNIDADES_BASICAS = (
        (GRAMO, "g"),
        (CM3, "cm3"),
        (UNIDAD, "unidad"),
        (METRO, "metro"),
        (METRO2, "metro2")
    )
    # Ejemplos: Remaches, Lijas, Fibra, Resina, Pintura, Masilla, Cinta
    nombre = models.CharField(max_length=50, unique=True)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES_BASICAS)

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(TipoMaterial,"nombre",self.nombre)
        return super().clean()
     

class Material(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    def menos_stock(self, cantidad):
        self.cantidad -= cantidad
        self.save()

    def stock(self):
        return self.cantidad

    def calcular_precio(self, cantidad):
        return self.precio * cantidad


class Cliente(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    def vip(self):
        # Obtener ultimas tres facturas impagas del cliente
        facturas = self.facturas.all()
        if len(facturas) >= 3:
            facturas = self.facturas.filter(
                pagado=False).order_by('-fecha')[:3]
            return len(facturas) <= 3
        return False


class Vehiculo(models.Model):
    # Ejemplo: ABC-123 o AC-123-AA
    # TODO: Validar con patrones
    cliente = models.ForeignKey(
        Cliente, related_name="vehiculos", on_delete=models.CASCADE)
    patente = models.CharField(max_length=7, unique=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    anio = models.IntegerField()
    chasis = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.modelo} - {self.patente}"

class Empleado(models.Model):
    # Ejemplo: 21-17263542-2
    # TODO: Validar con patrones y digito verificador
    cuil = models.CharField(max_length=13, unique=True)
    legajo = models.IntegerField(null=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    tareas = models.ManyToManyField(TipoTarea)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def crear_usuario(self):
        username = (self.nombre[0] + self.apellido).lower()
        user = User.objects.create_user(
            username=username, password=self.cuil, first_name=self.nombre, last_name=self.apellido)
        user.save()
        self.usuario = user
        return user


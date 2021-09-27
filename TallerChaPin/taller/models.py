from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# http://....../?atributo__contains=valor
# FILTRO = {'atributo__contains': valor}
# ...?nombre__icontains=a&marca__exact=1


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


class ModeloQuerySet(models.QuerySet):
    def filtrar(self, texto):
        return self.filter(texto_to_query(texto))


class Modelo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    marca = models.ForeignKey(
        Marca, related_name="modelos", on_delete=models.CASCADE)
    objects = ModeloQuerySet.as_manager()

    def __str__(self):
        return self.nombre


class TipoTarea(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    # Requiere Material[si/no]
    materiales = models.BooleanField(default=False)
    # Requiere Repuesto[si/no]
    repuestos = models.BooleanField(default=False)
    # Requiere Planilla[si/no]
    planilla = models.BooleanField(default=False)
    pass


class Tarea(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)


class TipoRepuesto(models.Model):
    pass


class Repuesto(models.Model):
    tipo = models.ForeignKey(TipoRepuesto, on_delete=models.CASCADE)


class TipoMaterial(models.Model):
    pass


class Material(models.Model):
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE)


class Cliente(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)


class Vehiculo(models.Model):
    # Ejemplo: ABC-123 o AC-123-AA
    # TODO: Validar con patrones
    cliente = models.ForeignKey(
        Cliente, related_name="vehiculos", on_delete=models.CASCADE)
    patente = models.CharField(max_length=7, unique=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    anio = models.IntegerField()
    chasis = models.CharField(max_length=50)


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
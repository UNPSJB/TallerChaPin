from genericpath import exists
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator

# Create your models here.
# http://....../?atributo__contains=valor
# FILTRO = {'atributo__contains': valor}
# ...?nombre__icontains=a&marca__exact=1


def validacion_nombre_unico(modelo, campo, value):
    aux = dict([(f"{campo}__iregex", f'^{value}$')])
    if modelo.objects.filter(**aux).exists():
        raise ValidationError({"nombre": "nombre ya existe"}) #TODO: se muestran con un formato malo
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
    descripcion = models.CharField(max_length=200, blank=True)
    objects = MarcaQuerySet.as_manager()

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(Marca, "nombre", self.nombre)
        return super().clean()


class ModeloQuerySet(models.QuerySet):
    def filtrar(self, texto):
        return self.filter(texto_to_query(texto))

def anio_valido(anio):
    if anio > date.today().year:
        raise ValidationError('El año del modelo no puede ser mayor al año actual')
class Modelo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    marca = models.ForeignKey(
        Marca, related_name="modelos", on_delete=models.RESTRICT)
    anio = models.PositiveSmallIntegerField(validators=[anio_valido])

    # Manager de la clase Modelo
    objects = ModeloQuerySet.as_manager()

    def __str__(self):
        return f"{self.nombre}, {self.marca}"

    def clean(self) -> None:
        validacion_nombre_unico(Modelo, "nombre", self.nombre)
        return super().clean()


class TipoTarea(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    # Requiere Material[si/no]
    materiales = models.BooleanField(default=False)
    # Requiere Repuesto[si/no]
    repuestos = models.BooleanField(default=False)
    # Requiere Planilla[si/no]
    planilla = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def clean(self) -> None:
        validacion_nombre_unico(TipoTarea, "nombre", self.nombre)
        return super().clean()

    def get_req_materiales(self):
        return self.materiales
    
    def get_req_repuestos(self):
        return self.repuestos
    
    def get_req_planilla(self):
        return self.planilla

class Tarea(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    tipo = models.ForeignKey(TipoTarea, on_delete=models.RESTRICT)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators = [MinValueValidator(0)])

    def __str__(self):
        return self.nombre

    def eliminable(self, presupuesto_id):
        presupuestos = self.presupuestos.filter(pk=presupuesto_id)
        if presupuestos.exists():
            presupuesto = presupuestos.first()
            if presupuesto.orden:
                detalles = presupuesto.orden.detalles.filter(tarea=self)
                return not (detalles.exists() and detalles.first().exitosa)
        return True

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
    modelo = models.ForeignKey(Modelo, on_delete=models.RESTRICT)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    cantidad = models.IntegerField(blank=True, null=True, default=0, validators = [MinValueValidator(0)])
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators = [MinValueValidator(0)])

    def __str__(self):
        return f"{self.nombre}, {self.modelo}"

    def get_tipo(self):
        return self.get_tipo_display()
    
    def decrementar_stock(self,cantidad):
        self.cantidad -= cantidad
        self.save()

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
        (CM3, "CM3"),
        (UNIDAD, "Unidad/es"),  # Por unidad
        (METRO, "Metro/s"),
        (METRO2, "Metro2")
    )
    # Ejemplos: Remaches, Lijas, Fibra, Resina, Pintura, Masilla, Cinta
    nombre = models.CharField(max_length=50, unique=True)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES_BASICAS)

    def __str__(self):
        return self.nombre

    # def clean(self) -> None:
    #     validacion_nombre_unico(TipoMaterial, "nombre", self.nombre)
    #     return super().clean()
    def get_unidad_medida(self):
        return self.get_unidad_medida_display()


class Material(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(blank=True, null=True, default=0, validators = [MinValueValidator(0)])
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators = [MinValueValidator(0)])

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) {self.tipo.get_unidad_medida_display()}"

    def decrementar_stock(self, cantidad):
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
        return f'{self.nombre} {self.apellido} ({self.dni})'
        
    def get_nombre_abreviado(self):
        return f'{self.nombre[0]}. {self.apellido}'

    def vip(self):
        # Obtener ultimas tres facturas pagas del cliente
        # Ir a los presupuestos
        # Tomar un presupuesto
        # si ese presupuesto tiene una orden, esta confirmado
        # Si la orden tiene una factura, esta facturada
        # ver si las ultimas 3 facturas
        # si hay 3 facturas pagadas es vip, caso contrario no es vip 
        facturas = []
        for presupuesto in self.presupuestos.all():   
            if (presupuesto.orden) != None and (presupuesto.orden.factura) != None:              
                    facturas.extend(presupuesto.orden.factura.all())
            else:
                return False  
        # Veo las ultimas 4, puede adeudar al menos una al ser VIP
        facturas = sorted(facturas, key=lambda f: f.fecha , reverse=True)[:4]
        if len(facturas) >= 4 and not facturas[0].pagado():
            facturas.pop(0) #De estar la mas reciente impaga la quita del listado. VER ESTO 
        return len(facturas) >= 3 and all(f.pagado() for f in facturas) 

def validar_anio(anio):
    if anio < date.today().year - 12:
        raise ValidationError('El vehículo tiene más de 12 años de antigüedad')
    if anio > date.today().year:
        raise ValidationError('El año del vehículo no puede ser mayor al año actual')

class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name="vehiculos", on_delete=models.RESTRICT)
    patente = models.CharField(max_length=7, unique=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.RESTRICT)
    anio = models.IntegerField(validators=[validar_anio])
    chasis = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.modelo} - {self.patente}"


class Empleado(models.Model):
    cuil = models.CharField(max_length=13, unique=True)
    legajo = models.IntegerField(null=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    tareas = models.ManyToManyField(TipoTarea, related_name="empleados")
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def crear_usuario(self):
        username = (self.nombre[0] + self.apellido).lower()
        user = User.objects.create_user(
            username=username, password=self.cuil, first_name=self.nombre, last_name=self.apellido)
        user.save()
        self.usuario = user
        self.save()
        return user

    def tiene_usuario(self):
        print(f'Usuario es none?: {self.usuario is not None}, usuario: {self.usuario} ')
        return self.usuario is not None

    def puede_hacer(self, tipo):
        return self.tareas.filter(id=tipo.id).exists()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

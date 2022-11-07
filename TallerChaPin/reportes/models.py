from datetime import timedelta
from django.utils.timezone import now
from django.utils import timezone
from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto,
    Marca
)
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

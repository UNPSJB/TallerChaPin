# Generated by Django 3.2.6 on 2021-11-10 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0008_alter_empleado_tareas'),
        ('ordenes', '0002_auto_20211004_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordendetrabajo',
            options={'permissions': [('can_registrar_ingreso', 'Puede registrar el ingreso de un vehiculo al taller'), ('can_asignar_trabajo', 'Puede asignar trabajo a empleados')]},
        ),
        migrations.AlterField(
            model_name='detalleordendetrabajo',
            name='empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trabajo', to='taller.empleado'),
        ),
    ]

# Generated by Django 3.2.6 on 2021-12-03 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0010_delete_tiporepuesto'),
        ('ordenes', '0003_auto_20211110_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordendetrabajo',
            options={'permissions': [('can_registrar_ingreso', 'Puede registrar el ingreso de un vehículo al taller'), ('can_asignar_trabajo', 'Puede asignar trabajo a empleados')]},
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='detalles',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name='TurnoOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Turno', to='taller.cliente')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Turno', to='taller.vehiculo')),
            ],
        ),
    ]

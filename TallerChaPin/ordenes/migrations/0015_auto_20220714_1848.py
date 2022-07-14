# Generated by Django 3.2.6 on 2022-07-14 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0013_alter_tipomaterial_nombre'),
        ('ordenes', '0014_auto_20220714_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='materiales',
            field=models.ManyToManyField(through='ordenes.PresupuestoMaterial', to='taller.Material'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='repuestos',
            field=models.ManyToManyField(through='ordenes.PresupuestoRepuesto', to='taller.Repuesto'),
        ),
    ]

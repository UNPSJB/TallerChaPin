# Generated by Django 3.2.6 on 2022-05-28 18:43

from django.db import migrations, models
import ordenes.models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0006_presupuesto_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuestorepuesto',
            name='cantidad',
            field=models.PositiveBigIntegerField(validators=[ordenes.models.cantidad_positiva]),
        ),
    ]
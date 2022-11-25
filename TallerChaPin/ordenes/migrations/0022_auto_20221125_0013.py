# Generated by Django 3.2.6 on 2022-11-25 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0021_alter_presupuesto_vehiculo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialordendetrabajo',
            old_name='cantidad',
            new_name='cantidad_presupuestada',
        ),
        migrations.RenameField(
            model_name='repuestoordendetrabajo',
            old_name='cantidad',
            new_name='cantidad_presupuestada',
        ),
        migrations.AddField(
            model_name='materialordendetrabajo',
            name='cantidad_utilizada',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='repuestoordendetrabajo',
            name='cantidad_utilizada',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]

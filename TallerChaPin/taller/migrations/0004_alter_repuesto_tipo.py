# Generated by Django 3.2.6 on 2021-10-25 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0003_auto_20211025_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuesto',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Puerta'), (2, 'Guardabarros'), (3, 'Parabrisa'), (4, 'Cristal'), (5, 'Bateria'), (6, 'Rueda'), (7, 'Mecanico'), (8, 'Llanta'), (9, 'Suspension'), (10, 'Aire Acondicionado'), (99, 'Otro')]),
        ),
    ]

# Generated by Django 3.2.6 on 2021-11-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0005_merge_20211101_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuesto',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Puerta'), (2, 'Guardabarros'), (3, 'Parabrisa'), (4, 'Cristal'), (5, 'Bateria'), (6, 'Rueda'), (7, 'Mecanico'), (8, 'Llanta'), (9, 'Suspension'), (10, 'Aire Acondicionado'), (99, 'Otro')]),
        ),
    ]

# Generated by Django 3.2.6 on 2021-10-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0002_alter_repuesto_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuesto',
            name='tipo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tipomaterial',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

# Generated by Django 3.2.6 on 2022-05-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0012_alter_tipomaterial_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipomaterial',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

# Generated by Django 3.2.6 on 2022-08-06 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0003_factura_cuotas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='cuotas',
            field=models.PositiveSmallIntegerField(default=1, null=True),
        ),
    ]

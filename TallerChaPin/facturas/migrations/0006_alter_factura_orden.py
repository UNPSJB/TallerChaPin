# Generated by Django 3.2.6 on 2022-08-28 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0018_auto_20220728_2017'),
        ('facturas', '0005_auto_20220806_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='ordenes.ordendetrabajo'),
        ),
    ]

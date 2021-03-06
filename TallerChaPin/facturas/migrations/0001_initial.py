# Generated by Django 3.2.6 on 2021-10-06 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ordenes', '0002_auto_20211004_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.ordendetrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'Contado'), (1, 'Tarjeta Debito'), (2, 'Tarjeta Credito')], default=0)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='facturas.factura')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='facturas.factura')),
            ],
        ),
    ]

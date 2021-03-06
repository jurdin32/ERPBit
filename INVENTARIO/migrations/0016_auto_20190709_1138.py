# Generated by Django 2.0 on 2019-07-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVENTARIO', '0015_auto_20190214_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleproproveedor',
            name='codigoICE',
            field=models.CharField(default=0.0, max_length=10),
        ),
        migrations.AlterField(
            model_name='detalleproproveedor',
            name='codigoIRBPNR',
            field=models.CharField(default=0.0, max_length=10),
        ),
        migrations.AlterField(
            model_name='detalleproproveedor',
            name='codigoIVA',
            field=models.CharField(default=0.0, max_length=10),
        ),
        migrations.AlterField(
            model_name='detalleproproveedor',
            name='ice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]

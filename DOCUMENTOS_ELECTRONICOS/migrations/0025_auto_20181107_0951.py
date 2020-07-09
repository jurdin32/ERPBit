# Generated by Django 2.0 on 2018-11-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0024_auto_20181105_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosdocumentos',
            name='secuencialNotaVenta',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='factura',
            name='tipo',
            field=models.CharField(choices=[('FACTURA', 'FACTURA'), ('PROFORMA', 'PROFORMA'), ('NOTA DE VENTA', 'NOTA DE VENTA')], max_length=20),
        ),
    ]

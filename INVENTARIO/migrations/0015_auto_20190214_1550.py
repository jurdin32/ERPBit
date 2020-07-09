# Generated by Django 2.0 on 2019-02-14 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVENTARIO', '0014_kardex_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kardex',
            name='stockmax',
        ),
        migrations.RemoveField(
            model_name='kardex',
            name='stockmin',
        ),
        migrations.AddField(
            model_name='detalleproproveedor',
            name='stockmax',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='detalleproproveedor',
            name='stockmin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

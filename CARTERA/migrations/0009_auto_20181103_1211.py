# Generated by Django 2.0 on 2018-11-03 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CARTERA', '0008_cuentasporcobrar_detallescuentascobrar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasporcobrar',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='detallescuentascobrar',
            name='cuenta',
        ),
        migrations.RemoveField(
            model_name='detallescuentascobrar',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='CuentasPorCobrar',
        ),
        migrations.DeleteModel(
            name='DetallesCuentasCobrar',
        ),
    ]

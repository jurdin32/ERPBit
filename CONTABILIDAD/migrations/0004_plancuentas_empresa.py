# Generated by Django 2.0 on 2018-11-11 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0006_auto_20181109_1841'),
        ('CONTABILIDAD', '0003_auto_20181110_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='plancuentas',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa'),
        ),
    ]

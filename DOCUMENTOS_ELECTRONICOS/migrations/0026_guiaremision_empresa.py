# Generated by Django 2.0 on 2018-11-17 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0006_auto_20181109_1841'),
        ('DOCUMENTOS_ELECTRONICOS', '0025_auto_20181107_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='guiaremision',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa'),
        ),
    ]

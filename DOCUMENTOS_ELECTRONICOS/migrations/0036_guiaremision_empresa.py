# Generated by Django 2.0 on 2018-12-23 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0029_helpers_horafecha'),
        ('DOCUMENTOS_ELECTRONICOS', '0035_auto_20181222_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='guiaremision',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa'),
        ),
    ]

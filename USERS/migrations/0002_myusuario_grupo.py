# Generated by Django 2.0 on 2018-10-08 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0003_auto_20181006_2113'),
        ('USERS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusuario',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.Grupo'),
        ),
    ]

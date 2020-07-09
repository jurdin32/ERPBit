# Generated by Django 2.0 on 2018-12-14 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0011_auto_20181214_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
                ('funcion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.Funciones')),
            ],
        ),
    ]

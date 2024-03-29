# Generated by Django 2.0 on 2018-12-23 14:41

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0022_funciones_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Helpers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Titulos', max_length=150)),
                ('imagen', models.ImageField(upload_to='helpers')),
            ],
        ),
        migrations.CreateModel(
            name='HelpersDetalles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitulo', models.CharField(max_length=150)),
                ('detalles', tinymce.models.HTMLField()),
            ],
        ),
    ]

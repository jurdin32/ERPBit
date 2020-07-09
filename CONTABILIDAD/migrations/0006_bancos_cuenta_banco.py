# Generated by Django 2.0 on 2018-12-25 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONTABILIDAD', '0005_auto_20181111_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bancos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta_Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_cuenta', models.CharField(max_length=15)),
                ('tipo_cuenta', models.CharField(choices=[('A', 'AHORRO'), ('C', 'CORRIENTE')], max_length=50)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CONTABILIDAD.Bancos')),
            ],
        ),
    ]

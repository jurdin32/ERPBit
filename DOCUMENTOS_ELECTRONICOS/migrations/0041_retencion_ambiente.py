# Generated by Django 2.0 on 2018-12-24 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0040_retencion_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='retencion',
            name='ambiente',
            field=models.CharField(blank=True, default=1, max_length=10, null=True),
        ),
    ]

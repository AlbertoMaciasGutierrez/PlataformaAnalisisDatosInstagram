# Generated by Django 4.0.3 on 2022-07-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0017_datosvideosbusquedausuario_datospostbusquedausuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datospostbusquedausuario',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
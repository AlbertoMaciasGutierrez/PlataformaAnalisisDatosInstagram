# Generated by Django 4.0.3 on 2022-08-03 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0028_datosbusquedausuario_numeroimagenespostrecientes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosbusquedausuario',
            name='numeroVideos',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
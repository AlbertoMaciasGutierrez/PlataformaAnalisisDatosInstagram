# Generated by Django 4.0.3 on 2022-06-15 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idsesionusuario',
            old_name='user',
            new_name='usuario',
        ),
    ]

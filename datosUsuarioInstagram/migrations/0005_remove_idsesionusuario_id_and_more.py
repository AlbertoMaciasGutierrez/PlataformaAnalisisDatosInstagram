# Generated by Django 4.0.3 on 2022-06-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0004_alter_idsesionusuario_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idsesionusuario',
            name='id',
        ),
        migrations.AlterField(
            model_name='idsesionusuario',
            name='content',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]

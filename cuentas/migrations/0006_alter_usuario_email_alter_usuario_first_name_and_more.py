# Generated by Django 4.0.3 on 2022-06-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0005_remove_usuario_prueba_alter_usuario_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='correo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='last_name',
            field=models.TextField(max_length=100, verbose_name='apellidos'),
        ),
    ]
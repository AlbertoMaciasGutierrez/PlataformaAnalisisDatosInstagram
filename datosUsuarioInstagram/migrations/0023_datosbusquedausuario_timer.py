# Generated by Django 4.0.3 on 2022-07-28 17:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0022_datoshighlight_datosstoryhighlight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosbusquedausuario',
            name='timer',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 7, 28, 17, 27, 53, 100358, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.0.3 on 2022-08-03 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datosUsuarioInstagram', '0029_datosbusquedausuario_numerovideos'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosPost',
            fields=[
                ('shortcode', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('likes', models.IntegerField()),
                ('comentarios', models.IntegerField()),
                ('tipo', models.CharField(max_length=20)),
                ('fecha', models.DateTimeField()),
                ('propietario', models.CharField(max_length=100)),
                ('numero_publicaciones', models.IntegerField()),
                ('patrocinado', models.BooleanField()),
                ('post_fijado', models.BooleanField()),
                ('url', models.TextField()),
                ('numeroVideos', models.IntegerField()),
                ('numeroImagenes', models.IntegerField()),
                ('titulo', models.CharField(blank=True, max_length=100)),
                ('subtitulo', models.TextField(blank=True)),
                ('ubicacion', models.CharField(blank=True, max_length=100)),
                ('duracion', models.FloatField()),
                ('timer', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosEtiquetadosPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Usuarios etiquetados en publicación',
                'verbose_name_plural': 'Usuarios etiquetados en publicaciones',
            },
        ),
        migrations.CreateModel(
            name='UsuarioMaxComentariosPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('comentarios', models.IntegerField()),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Usuario que más comenta en publicación',
                'verbose_name_plural': 'Usuarios que más comentan en publicaciones',
            },
        ),
        migrations.CreateModel(
            name='PostSidecar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('tipo', models.CharField(max_length=20)),
                ('url', models.TextField()),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Publicación Sidecar',
                'verbose_name_plural': 'Publicaciones Sidecar',
            },
        ),
        migrations.CreateModel(
            name='PatrocinadoresPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patrocinador', models.CharField(max_length=100)),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Patrocinadores en publicación',
                'verbose_name_plural': 'Patrocinadores en publicaciones',
            },
        ),
        migrations.CreateModel(
            name='MencionesSubtituloPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mencion', models.CharField(max_length=100)),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Menciones en subtítulo de publicación',
                'verbose_name_plural': 'Menciones en subtítulos de publicaciones',
            },
        ),
        migrations.CreateModel(
            name='HashtagsSubtituloPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=100)),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Hashtags en subtítulo de publicación',
                'verbose_name_plural': 'Hashtags en subtítulos de publicación',
            },
        ),
        migrations.CreateModel(
            name='ComentarioMaxLikesPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propietario', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField()),
                ('likes', models.IntegerField()),
                ('text', models.TextField()),
                ('shortcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datosUsuarioInstagram.datospost')),
            ],
            options={
                'verbose_name': 'Comentario con más likes en publicación',
                'verbose_name_plural': 'Comentarios con más likes en publicaciones',
            },
        ),
    ]
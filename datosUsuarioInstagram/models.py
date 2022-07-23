from os import device_encoding
from sqlite3 import Timestamp
from tabnanny import verbose
from django.db import models
from cuentas.models import Usuario
from django.utils import timezone


class IDSesionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    content = models.TextField()
    add_fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'IDSesionUsuario'
        verbose_name_plural = 'IDSesionUsuarios'
        ordering = ['-add_fecha']

    def __str__(self):
        return f'El IDSesion de {self.usuario} es {self.content}' 

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    mensaje = models.TextField()
    
    def __str__(self):
        return self.nombre


class DatosBusquedaUsuario(models.Model):
    IDcuenta = models.CharField(primary_key=True, max_length=100)
    Nombre = models.TextField(blank=True)
    Usuario_verificado = models.BooleanField()
    Popularidad = models.IntegerField()
    Perfil = models.TextField()
    Usuario_privado = models.BooleanField()
    Cuenta_negocios = models.BooleanField()
    Publicaciones = models.IntegerField()
    Biografia = models.TextField(blank=True)
    Foto_perfil = models.TextField(blank=True)
    Videos = models.IntegerField()
    Website = models.TextField(null=True, blank=True)
    #POST
    mediaLikesPostRecientes = models.FloatField()
    mediaComentariosPostRecientes = models.FloatField()
    #VIDEOS
    mediaLikesVideos = models.FloatField()
    mediaComentariosVideos = models.FloatField()
    mediaVisualizacionesVideos = models.FloatField()
    #ETIQUETADAS
    mediaLikesPublicacionesEtiquetadas = models.FloatField()
    mediaComentariosPublicacionesEtiquetadas = models.FloatField()
    

    def __str__(self):
        return self.IDcuenta


class DatosPostBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.CharField(max_length=20)
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"


class DatosVideosBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    reproducciones = models.IntegerField()
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    fecha = models.CharField(max_length=20)
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.fecha}"


class DatosEtiquetadasBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.CharField(max_length=20)
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"



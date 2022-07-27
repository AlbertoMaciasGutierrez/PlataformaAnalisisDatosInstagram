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

##--------------------------------------------------------------------##
##-------------------------Busqueda de perfil-------------------------##
##--------------------------------------------------------------------##

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
    fecha = models.DateTimeField()
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"


class DatosVideosBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    reproducciones = models.IntegerField()
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    fecha = models.DateTimeField()
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.fecha}"


class DatosEtiquetadasBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    url = models.TextField()

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"

    class Meta:
        verbose_name = "Datos post etiquetados busqueda de usuario"


##------------------------------------------------------------------------##
##-------------------------Busqueda de highlights-------------------------##
##------------------------------------------------------------------------##

class IdentificadorUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    usuarioID = models.IntegerField()

    def __str__(self):
        return f" {self.cuentaID} con ID Usuario de {self.usuarioID}"
    
    class Meta:
        verbose_name = "ID usuario"

#'''
class ContadorHighlights(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    contadorHighlights = models.IntegerField()

    def __str__(self):
        return f" {self.cuentaID} - {self.contadorHighlights} highlights"
    
    class Meta:
        verbose_name = "Contador highlights cuenta"

class DatosHighlight(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    identificador_highlight_usuario = models.CharField(primary_key=True, max_length=50)
    titulo = models.CharField(max_length=30)
    numero_historias = models.IntegerField()
    foto_portada = models.TextField()
    url = models.TextField()
    numeroImagenes = models.IntegerField()
    numeroVideos = models.IntegerField()

    def __str__(self):
        return f" {self.cuentaID} highlight {self.titulo}"
    
    class Meta:
        verbose_name = "Highlight"


class DatosStoryHighlight(models.Model):
    highlight = models.ForeignKey(DatosHighlight, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    duracion = models.FloatField()
    url = models.TextField()

    def __str__(self):
        return f" {self.highlight} - {self.tipo} - {self.duracion} - {self.fecha}"
    
    class Meta:
        verbose_name = "Historias highlight" 
        
        
#'''


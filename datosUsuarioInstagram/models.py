from django.db import models
from cuentas.models import Usuario
from django.utils import timezone



class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    mensaje = models.TextField()
    
    def __str__(self):
        return self.nombre



##----------------------------------------------------------------------##
##-----------------------Cuentas Scrapeo Instagram----------------------##
##----------------------------------------------------------------------##

class CuentaScrapeoInstagram(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cuenta = models.CharField(max_length=100)
    usando = models.BooleanField()
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Cuenta Scrapeo Instagram'
        verbose_name_plural = 'Cuentas Scrapeo Instagram'
        ordering = ['-fecha']

    def __str__(self):
        return f'Cuenta Scraping Instagram del usuario "{self.usuario}"--> {self.cuenta}' 


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
    numeroImagenesPostRecientes = models.IntegerField()
    numeroVideosPostRecientes = models.IntegerField()
    numeroSidecarsPostRecientes = models.IntegerField()
    #VIDEOS
    mediaLikesVideos = models.FloatField()
    mediaComentariosVideos = models.FloatField()
    mediaVisualizacionesVideos = models.FloatField()
    numeroVideos = models.IntegerField()
    #ETIQUETADAS
    mediaLikesPublicacionesEtiquetadas = models.FloatField()
    mediaComentariosPublicacionesEtiquetadas = models.FloatField()
    numeroImagenesPublicacionesEtiquetadas = models.IntegerField()
    numeroVideosPublicacionesEtiquetadas = models.IntegerField()
    numeroSidecarsPublicacionesEtiquetadas = models.IntegerField()
    #TEMPORIZADOR
    timer = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.IDcuenta


class DatosPostBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    url = models.TextField()
    shortcode = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"


class DatosVideosBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    reproducciones = models.IntegerField()
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    fecha = models.DateTimeField()
    url = models.TextField()
    shortcode = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.cuentaID} - {self.fecha}"


class DatosEtiquetadasBusquedaUsuario(models.Model):
    cuentaID = models.ForeignKey(DatosBusquedaUsuario, on_delete=models.CASCADE)
    likes= models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    url = models.TextField()
    shortcode = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.cuentaID} - {self.tipo} - {self.fecha}"

    class Meta:
        verbose_name = "Datos post etiquetados busqueda de usuario"



##------------------------------------------------------------------------##
##-------------------------Busqueda de highlights-------------------------##
##------------------------------------------------------------------------##

class IdentificadorUsuario(models.Model):
    cuentaID = models.OneToOneField(DatosBusquedaUsuario, on_delete=models.CASCADE)
    usuarioID = models.IntegerField()

    def __str__(self):
        return f" {self.cuentaID} con ID Usuario de {self.usuarioID}"
    
    class Meta:
        verbose_name = "ID usuario"

#'''
class ContadorHighlights(models.Model):
    cuentaID = models.OneToOneField(DatosBusquedaUsuario, on_delete=models.CASCADE)
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



##----------------------------------------------------------------------##
##-------------------------Busqueda de publicación----------------------##
##----------------------------------------------------------------------##

class DatosPost(models.Model):
    shortcode = models.CharField(primary_key=True, max_length=100)
    likes = models.IntegerField()
    comentarios = models.IntegerField()
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    propietario = models.CharField(max_length=100)
    numero_publicaciones = models.IntegerField()
    patrocinado = models.BooleanField()
    post_fijado = models.BooleanField()
    url = models.TextField()
    #SIDECAR
    numeroVideos = models.IntegerField()
    numeroImagenes = models.IntegerField()

    titulo = models.CharField(max_length=100, blank=True)
    subtitulo = models.TextField(blank=True)
    ubicacion = models.CharField(blank=True, max_length=100)
    duracion = models.FloatField()
    #TEMPORIZADOR
    timer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shortcode

class ComentarioMaxLikesPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    propietario = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    likes = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f" {self.shortcode} - {self.propietario} -  {self.likes} - {self.fecha} "

    class Meta:
        verbose_name = "Comentario con más likes en publicación"
        verbose_name_plural = "Comentarios con más likes en publicaciones"


class UsuarioMaxComentariosPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    comentarios = models.IntegerField()

    def __str__(self):
        return f" {self.shortcode} - {self.nombre} -  {self.comentarios}"

    class Meta:
        verbose_name = "Usuario que más comenta en publicación"
        verbose_name_plural = "Usuarios que más comentan en publicaciones"

class PostSidecar(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=20)
    url = models.TextField()

    def __str__(self):
        return f" {self.shortcode} - {self.tipo} -  {self.numero}"

    class Meta:
        verbose_name = "Publicación Sidecar"
        verbose_name_plural = "Publicaciones Sidecar"


class HashtagsSubtituloPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=100)

    def __str__(self):
            return f" {self.shortcode} - {self.hashtag}"

    class Meta:
        verbose_name = "Hashtags en subtítulo de publicación"
        verbose_name_plural = "Hashtags en subtítulos de publicación"

class MencionesSubtituloPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    mencion = models.CharField(max_length=100)

    def __str__(self):
            return f" {self.shortcode} - {self.mencion}"

    class Meta:
        verbose_name = "Menciones en subtítulo de publicación"
        verbose_name_plural = "Menciones en subtítulos de publicaciones"

class PatrocinadoresPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    patrocinador = models.CharField(max_length=100)

    def __str__(self):
            return f" {self.shortcode} - {self.patrocinador}"

    class Meta:
        verbose_name = "Patrocinadores en publicación"
        verbose_name_plural = "Patrocinadores en publicaciones"


class UsuariosEtiquetadosPost(models.Model):
    shortcode = models.ForeignKey(DatosPost, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)

    def __str__(self):
            return f" {self.shortcode} - {self.usuario}"

    class Meta:
        verbose_name = "Usuarios etiquetados en publicación"
        verbose_name_plural = "Usuarios etiquetados en publicaciones"
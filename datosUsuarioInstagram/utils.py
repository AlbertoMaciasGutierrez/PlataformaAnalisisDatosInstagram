##------------------------------------------------------------------------------------##
##----------------------------Clases para los tipos de datos--------------------------##
##------------------------------------------------------------------------------------##

class PostClass:

    def __init__(self,cuentaID, likes, comentarios, tipo, fecha, url):
        self.cuentaID = cuentaID
        self.likes = likes
        self.comentarios = comentarios
        self.tipo = tipo
        self.fecha = fecha
        self.url = url

    def __repr__(self):
        return '{' + str(self.cuentaID) + ', ' + str(self.likes) + ', ' + str(self.comentarios) + ', ' + self.tipo + ', ' + str(self.fecha) + ', '+ self.url +'}'

class PostClassVideo:

    def __init__(self,cuentaID, reproducciones, likes, comentarios, fecha, url):
        self.cuentaID = cuentaID
        self.reproducciones = reproducciones
        self.likes = likes
        self.comentarios = comentarios
        self.fecha = fecha
        self.url = url

    def __repr__(self):
        return '{' + str(self.cuentaID) + ', ' + str(self.reproducciones) + ', ' + str(self.likes) + ', ' + str(self.comentarios) + ', ' + str(self.fecha) + ', '+ self.url +'}'

class HihglightClass:

    def __init__(self, titulo, numero_historias, foto_portada, url, numeroImagenes, numeroVideos, listaHistoriasDestacadas):
        self.titulo = titulo
        self.numero_historias = numero_historias
        self.foto_portada = foto_portada
        self.url = url
        self.numeroImagenes = numeroImagenes
        self.numeroVideos = numeroVideos
        self.listaHistoriasDestacadas = listaHistoriasDestacadas

    def __repr__(self):
        return '{' + self.titulo +  ', ' + str(self.numero_historias) + ', ' + self.foto_portada +  ', '+ self.url + ', '+ str(self.numeroImagenes) +  ', ' + str(self.numeroVideos) + '}'

class StoryClass:

    def __init__(self, tipo, fecha, duracion, url):
        self.tipo = tipo
        self.fecha = fecha
        self.duracion = duracion
        self.url = url

    def __repr__(self):
        return '{' + self.tipo +  ', ' + str(self.fecha) + ', ' + str(self.duracion) +  ', '+ self.url +'}'




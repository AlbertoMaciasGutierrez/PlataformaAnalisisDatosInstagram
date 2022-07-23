from sre_constants import IN
from instaloader import Instaloader, Profile
import traceback

#USER = 'instaanalysistfg'
#PASS = 'juliogamer0423'
INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'


L =Instaloader()
#L.login(USER,PASS)                            #Loguearse
#L.save_session_to_file()                      #Guardar sesión en archivo para no tener que volver a loguearnos
L.load_session_from_file('instaanalysistfg')  #Carga la sesión guardada del inicio de sesión anterior. Descomentar y comentar las dos líneas de arriba cuando esté guardada la sesión


##--------------------------------------------------------------------------##
##----------------------------Clase para los Posts--------------------------##
##--------------------------------------------------------------------------##

#Clase para introducir este tipo de objetos en la lista
class PostClass:

    def __init__(self,cuentaID, likes, comentarios, tipo, fecha, url):
        self.cuentaID = cuentaID
        self.likes = likes
        self.comentarios = comentarios
        self.tipo = tipo
        self.fecha = fecha
        self.url = url

    def __repr__(self):
        return '{' + str(self.cuentaID) + ', ' + str(self.likes) + ', ' + str(self.comentarios) + ', ' + self.tipo + ', ' + self.fecha + ', '+ self.url +'}'

class PostClassVideo:

    def __init__(self,cuentaID, reproducciones, likes, comentarios, fecha, url):
        self.cuentaID = cuentaID
        self.reproducciones = reproducciones
        self.likes = likes
        self.comentarios = comentarios
        self.fecha = fecha
        self.url = url

    def __repr__(self):
        return '{' + str(self.cuentaID) + ', ' + str(self.reproducciones) + ', ' + str(self.likes) + ', ' + str(self.comentarios) + ', ' + self.fecha + ', '+ self.url +'}'




##--------------------------------------------------------------------##
##-------------------------Busqueda de perfil-------------------------##
##--------------------------------------------------------------------##

def informacionCuenta(cuenta):
    try:


        profile = Profile.from_username(L.context, cuenta)

        context = {}
        
        url_perfil = INSTAGRAM + profile.username + '/'

        datos = {
        "Nombre": profile.full_name,
        "Usuario_verificado": profile.is_verified,
        "Popularidad": profile.followers,
        "Perfil": url_perfil,
        "Usuario_privado": profile.is_private,
        "Cuenta_negocios": profile.is_business_account,
        "Publicaciones": profile.mediacount,
        "Biografia": profile.biography,
        "Foto_perfil":profile.profile_pic_url,
        "Videos": profile.igtvcount,
        }
        context.update(datos)
        #Para poder almacenar este campo dentro de la base de datos
        if (profile.external_url == None):
            context.update({"Website":''})
            print(context['Website'])
        else:
            context.update({"Website":profile.external_url})

        context_publicaciones= obtenerComentariosLikesPosts(profile,cuenta)
        context_videos = obtenerComentariosLikesVideos(profile,cuenta)
        context_publicaciones_etiquetadas = obtenerComentariosLikesPublicacionesEtiquetadas(profile,cuenta)

        context.update(context_publicaciones)
        context.update(context_videos)
        context.update(context_publicaciones_etiquetadas)


        return context
    except Exception as e: 
        traceback.print_exc()
        return None




def obtenerComentariosLikesPosts(profile,cuenta):
    
    publicaciones = profile.get_posts()               #muestra las publicaciones de la cuenta                    
    
    listaInfoPostRecientes = []

    mediaLikes = 0
    mediaComentarios = 0
    #mediaPublicacionesDia = 0

    contador = 0                    #Número de publicaciones mostradas
    contadorPublicaciones = 0
    tipo_publicacion = ''

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de publicaciones a mostrar como máximo

        dia_publicacion = str(post.date_local.day)
        mes_publicacion = str(post.date_local.month)
        anio_publicacion = str(post.date_local.year)

        fecha_publicacion = dia_publicacion + "/" + mes_publicacion + "/" + anio_publicacion

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): tipo_publicacion ='Imagen'
        elif(post.typename == 'GraphVideo'): tipo_publicacion ='Video'
        else: tipo_publicacion ='Sidecar'
        
        listaInfoPostRecientes.append(PostClass(cuenta, post.likes, post.comments, tipo_publicacion, fecha_publicacion, url_post))
        contadorPublicaciones+=1


    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)
        
        #Para calcular la media de publicaciones al día
        """fecha1 = datetime.now()
        fecha2 = datetime.strptime(likesComentarios[-1][2],'%d/%m/%Y')
        diferenciaDias = (fecha1-fecha2) /timedelta(days =1)
        mediaPublicacionesDia = round(contadorPublicaciones/ diferenciaDias,5)"""

    

    context ={
        'listaInfoPostRecientes': listaInfoPostRecientes,
        'mediaLikesPostRecientes': mediaLikes,
        'mediaComentariosPostRecientes': mediaComentarios,
        #'mediaPublicacionesDia': mediaPublicacionesDia
    }

    return context




def obtenerComentariosLikesVideos(profile, cuenta):
    
    publicaciones = profile.get_igtv_posts()               #muestra los vídeos de la cuenta                    
    
    listaInfoVideos = []

    mediaLikes = 0
    mediaComentarios = 0
    mediaVisualizaciones = 0

    contador = 0                    #Número de publicaciones mostradas

    contadorPublicaciones = 0

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de videos a mostrar como máximo

        dia_publicacion = str(post.date_local.day)
        mes_publicacion = str(post.date_local.month)
        anio_publicacion = str(post.date_local.year)

        fecha_publicacion = dia_publicacion + "/" + mes_publicacion + "/" + anio_publicacion

        mediaLikes += post.likes
        mediaComentarios += post.comments
        mediaVisualizaciones += post.video_view_count

        url_post = INSTAGRAM + POST + post.shortcode + '/'
        listaInfoVideos.append(PostClassVideo(cuenta, post.video_view_count, post.likes, post.comments, fecha_publicacion, url_post))
        contadorPublicaciones+=1


    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)
        mediaVisualizaciones = round(mediaVisualizaciones/contadorPublicaciones,2)
        
    context ={
        'listaInfoVideos': listaInfoVideos,
        'mediaLikesVideos': mediaLikes,
        'mediaComentariosVideos': mediaComentarios,
        'mediaVisualizacionesVideos': mediaVisualizaciones,
    }

    return context



def obtenerComentariosLikesPublicacionesEtiquetadas(profile, cuenta):
    
    publicaciones = profile.get_tagged_posts()              #muestra publicaciones en las que está etiquetada dicha cuenta                   
    
    listaInfoPublicacionesEtiquetadas = []

    mediaLikes = 0
    mediaComentarios = 0

    contador = 0                    #Número de publicaciones mostradas
    contadorPublicaciones = 0

    tipo_publicacion =''

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de publicaciones a mostrar como máximo

        dia_publicacion = str(post.date_local.day)
        mes_publicacion = str(post.date_local.month)
        anio_publicacion = str(post.date_local.year)

        fecha_publicacion = dia_publicacion + "/" + mes_publicacion + "/" + anio_publicacion

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): tipo_publicacion ='Imagen'
        elif(post.typename == 'GraphVideo'): tipo_publicacion ='Video'
        else: tipo_publicacion ='Sidecar'

        listaInfoPublicacionesEtiquetadas.append(PostClass(cuenta, post.likes, post.comments, tipo_publicacion, fecha_publicacion, url_post))
        contadorPublicaciones+=1


    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)
        
    context ={
        'listaInfoPublicacionesEtiquetadas': listaInfoPublicacionesEtiquetadas,
        'mediaLikesPublicacionesEtiquetadas': mediaLikes,
        'mediaComentariosPublicacionesEtiquetadas': mediaComentarios,
    }

    return context
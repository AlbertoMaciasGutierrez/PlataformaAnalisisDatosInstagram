from sre_constants import IN
from instaloader import Instaloader, Profile
import traceback

USER = 'instaanalysistfg'
PASS = 'juliogamer04'
INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'

L =Instaloader()
L.login(USER,PASS)


##--------------------------------------------------------------------------##
##----------------------------Clase para los Posts--------------------------##
##--------------------------------------------------------------------------##

#Clase para introducir este tipo de objetos en la lista
class PostClass:
 
    def __init__(self, likes, comentarios, fecha, url):
        self.likes = likes
        self.comentarios = comentarios
        self.fecha = fecha
        self.url = url
 
    def __repr__(self):
        return '{' + str(self.likes) + ', ' + str(self.comentarios) + ', ' + self.fecha + ', '+ self.url +'}'




##--------------------------------------------------------------------##
##-------------------------Busqueda de perfil-------------------------##
##--------------------------------------------------------------------##

def informacionCuenta(cuenta):
    try:


        profile = Profile.from_username(L.context, cuenta)

        context = obtenerComentariosLikesPosts(profile)
        
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
        "Website":profile.external_url,
        "Rells": profile.igtvcount,
        }

        context['info'] = datos

        return context
    except Exception as e: 
        traceback.print_exc()
        return None




def obtenerComentariosLikesPosts(profile):
    
    publicaciones = profile.get_posts()
    
    listaInfoPosts = []

    mediaLikes = 0
    mediaComentarios = 0
    #mediaPublicacionesDia = 0

    contador = 0                    #Número de publicaciones mostradas

    contadorPublicaciones = 0

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
        listaInfoPosts.append(PostClass(post.likes, post.comments, fecha_publicacion, url_post))
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
        'listaInfoPosts': listaInfoPosts,
        'mediaLikes': mediaLikes,
        'mediaComentarios': mediaComentarios,
        #'mediaPublicacionesDia': mediaPublicacionesDia
    }

    return context
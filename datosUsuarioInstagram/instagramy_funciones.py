from instagramy import InstagramUser, InstagramHashTag, InstagramPost, InstagramLocation
from instagramy.plugins.analysis import analyze_users_popularity
import traceback
from datetime import datetime, timedelta

sesion_id = "52174686364%3A0SjYfiJdyj2gbi%3A21"         #instaanalysistfg      Arreglar más adelante el uso de sesión id
#sesion_id = "1358918301%3AzuJoghD0FN2DAg%3A24"          #macy_guty



##-----------------------------------------------------------------------##
##----------------------------CLASEPARALOSPOST---------------------------##
##-----------------------------------------------------------------------##

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
##----------------------------INSTAGRAMUSER---------------------------##
##--------------------------------------------------------------------##


def modificarSesion_id():
    return sesion_id



def informacionCuenta(cuenta):
    # Connecting the profile
    try:
        #user = InstagramUser(cuenta,sessionid=sesion_id)
        user = InstagramUser(cuenta,from_cache=False)         #->Sin el id de la sesion no funciona la búsqueda de perfiles privados o verificados 

        context = obtenerComentariosLikesPosts(user.posts)
        
        datos = {
        "Nombre": user.fullname,
        "Usuario_verificado": user.is_verified,
        "Popularidad": user.number_of_followers,
        "Perfil": user.url,
        "Usuario_privado": user.is_private,
        "Publicaciones": user.number_of_posts,
        "Biografia": user.biography,
        "Foto_perfil":user.profile_picture_url,
        "Website":user.website,
        "Email": user.user_data['business_email'],
        "Telefono": user.user_data['business_phone_number'],
        }

        context['info'] = datos

        return context
    except Exception as e: 
        traceback.print_exc()
        return None
    


def obtenerComentariosLikesPosts(posts):
    listaInfoPosts = []

    mediaLikes = 0
    mediaComentarios = 0
    #mediaPublicacionesDia = 0

    contadorPublicaciones = 0

    for post in posts:
        dia_publicacion = str(post.taken_at_timestamp.day)
        mes_publicacion = str(post.taken_at_timestamp.month)
        anio_publicacion = str(post.taken_at_timestamp.year)

        fecha_publicacion = dia_publicacion + "/" + mes_publicacion + "/" + anio_publicacion

        mediaLikes += post.likes
        mediaComentarios += post.comments
        listaInfoPosts.append(PostClass(post.likes, post.comments, fecha_publicacion, post.post_url))
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



##-----------------------------------------------------------------------##
##----------------------------INSTAGRAMHASHTAG---------------------------##
##-----------------------------------------------------------------------##

def informacionHashtag(hashtag):
    try:

        tag = InstagramHashTag(hashtag, from_cache=False)
        #tag = InstagramHashTag(hashtag, sessionid=sesion_id)
        
        context = postPopularesHashtag(tag.top_posts)
        

        datos = {
            'Busqueda': tag.url,
            'Publicaciones': tag.number_of_posts,
        }

        context['info'] = datos

        return context
    except Exception as e: 
        traceback.print_exc()
        return None

def postPopularesHashtag(posts):
    listaInfoPosts = []

    mediaLikes = 0
    mediaComentarios = 0

    contadorPublicaciones = 0

    for post in posts:
        dia_publicacion = str(post.upload_time.day)
        mes_publicacion = str(post.upload_time.month)
        anio_publicacion = str(post.upload_time.year)

        fecha_publicacion = dia_publicacion + "/" + mes_publicacion + "/" + anio_publicacion

        mediaLikes += post.likes
        mediaComentarios += post.comments
        listaInfoPosts.append(PostClass(post.likes, post.comments, fecha_publicacion, post.post_url))
        contadorPublicaciones+=1

    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)

        #listaInfoPosts.sort(key=lambda x: x.likes, reverse=True)
    
    context ={
        "listaInfoPosts":listaInfoPosts,
        'mediaLikes': mediaLikes,
        'mediaComentarios': mediaComentarios,
    }

    return context
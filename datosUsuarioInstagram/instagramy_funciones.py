from multiprocessing import context
from operator import pos
from instagramy import InstagramUser, InstagramHashTag, InstagramPost, InstagramLocation
from instagramy.plugins.analysis import analyze_users_popularity

sesion_id = "52174686364%3AlOUE15nY2hJRMW%3A15"         #instaanalysistfg      Arreglar más adelante el uso de sesión id
#sesion_id = "1358918301%3AzuJoghD0FN2DAg%3A24"          #macy_guty

##--------------------------------------------------------------------##
##----------------------------INSTAGRAMUSER---------------------------##
##--------------------------------------------------------------------##


def modificarSesion_id():
    return sesion_id



def informacionCuenta(cuenta):
    # Connecting the profile
    try:
        user = InstagramUser(cuenta,sessionid=sesion_id)
        #user = InstagramUser(cuenta,from_cache=True)         #->Sin el id de la sesion no funciona la búsqueda de perfiles privados o verificados 

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
        }

        context['info'] = datos

        return context
    except:
        return None
    


def obtenerComentariosLikesPosts(posts):
    likes = []
    comentarios = []
    likesComentarios = []

    mediaLikes = 0
    mediaComentarios = 0
    contadorPublicaciones = 0

    for post in posts:

        likes.append(post.likes)
        mediaLikes += post.likes
        comentarios.append(post.comments)
        mediaComentarios += post.comments
        listaTemporal = []
        listaTemporal.append(post.likes)
        listaTemporal.append(post.comments)
        likesComentarios.append(listaTemporal)
        contadorPublicaciones+=1

    mediaLikes = round(mediaLikes/contadorPublicaciones,2)
    mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)

    context ={
        'likesComentarios': likesComentarios,
        'likes': likes,
        'comentarios': comentarios,
        'mediaLikes': mediaLikes,
        'mediaComentarios': mediaComentarios
    }

    return context
    

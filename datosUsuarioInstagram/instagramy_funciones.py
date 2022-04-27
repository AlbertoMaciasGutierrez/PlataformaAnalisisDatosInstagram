from operator import pos
from instagramy import InstagramUser, InstagramHashTag, InstagramPost, InstagramLocation
from instagramy.plugins.analysis import analyze_users_popularity


##--------------------------------------------------------------------##
##----------------------------INSTAGRAMUSER---------------------------##
##--------------------------------------------------------------------##

def informacionCuenta(cuenta):
    # Connecting the profile 
    user = InstagramUser(cuenta,from_cache=True)
    otra_informacion = user.other_info
    posts = user.posts
    contadorPosts = 0

    datos = {
    "Nombre": user.fullname,
    "Usuario verificado": user.is_verified,
    "Popularidad": user.number_of_followers,
    "Perfil": user.url,
    }

    return datos


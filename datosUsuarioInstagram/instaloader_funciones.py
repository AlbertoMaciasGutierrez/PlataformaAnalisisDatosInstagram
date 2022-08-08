from instaloader import Instaloader, Profile, TopSearchResults, Post
import traceback
from datosUsuarioInstagram.utils import PostClass, PostClassVideo, HihglightClass, SidecarPostClass, StoryClass, UsuarioMaxComentariosClass, ComentarioMaxLikesClass
from time import monotonic

USER = 'instaanalysistfg'
PASS = 'juliogamer0404'
INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'
HIGHLIGHT = 'stories/highlights/'



L = Instaloader()
#L.login(USER,PASS)                            #Loguearse
#L.save_session_to_file()                      #Guardar sesión en archivo para no tener que volver a loguearnos
L.load_session_from_file('instaanalysistfg')  #Carga la sesión guardada del inicio de sesión anterior. Descomentar y comentar las dos líneas de arriba cuando esté guardada la sesión



##--------------------------------------------------------------------------##
##-------------------------Iniciar sesión Instagram-------------------------##
##--------------------------------------------------------------------------##
def iniciarSesion(user,contrasena):
    try:
        L = Instaloader()
        L.login(user,contrasena)
        L.save_session_to_file()
        return True

    except Exception as e: 
        traceback.print_exc()
        return False


def comprobarCuentaBuscadora(cuentaScrapeo):
    if(cuentaScrapeo == ''):
        cuentaBuscadora = L
        return cuentaBuscadora
    else:
        C = Instaloader()
        C.load_session_from_file(cuentaScrapeo)
        cuentaBuscadora = C
        return cuentaBuscadora


##--------------------------------------------------------------------##
##-------------------------Busqueda de perfil-------------------------##
##--------------------------------------------------------------------##

def buscadorPerfil(queryset,cuentaScrapeo):
    contador = 0
    listaPerfiles = []
    diccionarioPerfiles = {}

    cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)

    for perfil in TopSearchResults(cuentaBuscadora.context,queryset).get_profiles():
        contador += 1
        listaPerfiles.append(perfil.username)

    diccionarioPerfiles = {
    'contador': contador,
    'listaPerfiles': listaPerfiles
    }

    return diccionarioPerfiles


def informacionCuenta(cuenta,cuentaScrapeo):
    try:
        cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)

        profile = Profile.from_username(cuentaBuscadora.context, cuenta)

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
        "ID_usuario": profile.userid,
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

    numeroSidecars = numeroVideos = numeroImagenes = 0

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de publicaciones a mostrar como máximo

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): 
            tipo_publicacion ='Imagen'
            numeroImagenes +=1 
        elif(post.typename == 'GraphVideo'): 
            tipo_publicacion ='Video'
            numeroVideos +=1 
        else: 
            tipo_publicacion ='Sidecar'
            numeroSidecars +=1 
        
        #Para evitar que haya likes negativos
        if(post.likes < 0): likes = 0
        else: likes = post.likes

        listaInfoPostRecientes.append(PostClass(cuenta, likes, post.comments, tipo_publicacion, post.date_local, url_post, post.shortcode))
        contadorPublicaciones+=1


    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)
        

    context ={
        'listaInfoPostRecientes': listaInfoPostRecientes,
        'mediaLikesPostRecientes': mediaLikes,
        'mediaComentariosPostRecientes': mediaComentarios,
        'numeroImagenesPostRecientes': numeroImagenes,
        'numeroVideosPostRecientes': numeroVideos,
        'numeroSidecarsPostRecientes': numeroSidecars,
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

        mediaLikes += post.likes
        mediaComentarios += post.comments
        mediaVisualizaciones += post.video_view_count

        #Para evitar que haya likes negativos
        if(post.likes < 0): likes = 0
        else: likes = post.likes

        url_post = INSTAGRAM + POST + post.shortcode + '/'
        listaInfoVideos.append(PostClassVideo(cuenta, post.video_view_count, likes, post.comments, post.date_local, url_post, post.shortcode))
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
        'numeroVideos': contadorPublicaciones,
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

    numeroSidecars = numeroVideos = numeroImagenes = 0

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de publicaciones a mostrar como máximo

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): 
            tipo_publicacion ='Imagen'
            numeroImagenes +=1 
        elif(post.typename == 'GraphVideo'): 
            tipo_publicacion ='Video'
            numeroVideos +=1 
        else: 
            tipo_publicacion ='Sidecar'
            numeroSidecars +=1 

        #Para evitar que haya likes negativos
        if(post.likes < 0): likes = 0
        else: likes = post.likes

        listaInfoPublicacionesEtiquetadas.append(PostClass(cuenta, likes, post.comments, tipo_publicacion, post.date_local, url_post, post.shortcode))
        contadorPublicaciones+=1

    if(contadorPublicaciones !=0):
        mediaLikes = round(mediaLikes/contadorPublicaciones,2)
        mediaComentarios = round(mediaComentarios/contadorPublicaciones,2)
        
    context ={
        'listaInfoPublicacionesEtiquetadas': listaInfoPublicacionesEtiquetadas,
        'mediaLikesPublicacionesEtiquetadas': mediaLikes,
        'mediaComentariosPublicacionesEtiquetadas': mediaComentarios,
        'numeroImagenesPublicacionesEtiquetadas': numeroImagenes,
        'numeroVideosPublicacionesEtiquetadas': numeroVideos,
        'numeroSidecarsPublicacionesEtiquetadas': numeroSidecars,
    }

    return context


##-------------------------------------------------------------##
##-------------------------Publicación-------------------------##
##-------------------------------------------------------------##

def buscadorPost(queryset,cuentaScrapeo):
    try:
        cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)

        post = Post.from_shortcode(cuentaBuscadora.context, queryset)

        diccionarioPost = {
        'nombre': post.pcaption,
        'shortcode': post.shortcode
        }

        return diccionarioPost

    except Exception as e: 
        traceback.print_exc()
        return None


def informacionPost(IdentificadorPost,cuentaScrapeo):
    try:
        cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)

        post = Post.from_shortcode(cuentaBuscadora.context, IdentificadorPost)

        context = {}
        numeroImagenes = numeroVideos = 0

        if(post.typename == 'GraphImage'):
            tipo_publicacion ='Imagen'
            listaPostSidecar = []
        elif(post.typename == 'GraphVideo'): 
            tipo_publicacion ='Video'
            listaPostSidecar = []
        else: 
            tipo_publicacion ='Sidecar'
            listaPostSidecar, numeroVideos, numeroImagenes = obtenerPostSidecar(post)

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        context = {
            'shortcode': post.shortcode,
            'likes': post.likes,
            'comentarios': post.comments,
            'tipo': tipo_publicacion,
            'fecha': post.date_local,
            'propietario': post.owner_username,
            'numero_publicaciones': post.mediacount,
            'patrocinado': post.is_sponsored,
            'post_fijado': post.is_pinned,
            'url': url_post,
            'listaPostSidecar': listaPostSidecar,
            'numeroVideos': numeroVideos,
            'numeroImagenes': numeroImagenes,
        }

        if(post.pcaption == None):
            context['titulo'] = ''
        else:
            context['titulo'] = post.pcaption
        
        if(post.caption == None):
            context['subtitulo'] = ''
        else:
            context['subtitulo'] = post.caption

        if(post.location == None):
            context['ubicacion'] = ''
        else:
            context['ubicacion'] = post.location.name

        if(post.is_video):
            context['duracion'] = post.video_duration
        else:
            context['duracion'] = 0

        context['listaHastagsSustitulo'] = post.caption_hashtags
        context['listaMecionesSustitulo'] = post.caption_mentions
        context['listaPatrocinadoresPost'] = post.sponsor_users
        context['listaUsuariosEtiquetados'] = post.tagged_users

        context['comentarioMaxPopular'], context['usuarioMaxComenta'] = obtenerComentariosMasPopulares(post)

        return context

    except Exception as e: 
        traceback.print_exc()
        return None

def obtenerPostSidecar(post):
    lista = []
    contador = 0
    numeroVideos = numeroImagenes = 0
    for p in post.get_sidecar_nodes():
        contador += 1
        if(p.is_video):
            numeroVideos += 1
            tipo = 'Video'
            url = p.video_url
        else:
            numeroImagenes += 1
            tipo = 'Imagen'
            url = p.display_url

        lista.append(SidecarPostClass(contador,tipo,url))

    return lista, numeroVideos, numeroImagenes

def obtenerComentariosMasPopulares(post):
    contador = 0
    diccionarioComentariosUsuarios = {}
    comienzo = monotonic()                               #Temporizador para parar la ejecución si hay muchos comentarios
    maxComentarios = comentarioMaxLikes = tiempoTranscurrido = 0

    for c in post.get_comments():
        contador+=1
        fin = monotonic()
        tiempoTranscurrido = fin - comienzo
        #Temporizador de 30 segundos
        if(tiempoTranscurrido > 30):
            break

        if(contador == 1):
            comentarioMaxLikes = ComentarioMaxLikesClass(c.owner.username, c.created_at_utc, c.likes_count, c.text) 
            maxComentarios = UsuarioMaxComentariosClass(c.owner.username,1)
        elif(comentarioMaxLikes.likes < c.likes_count):
            comentarioMaxLikes = ComentarioMaxLikesClass(c.owner.username, c.created_at_utc, c.likes_count, c.text)
        
        if( c.owner.username in diccionarioComentariosUsuarios):
            diccionarioComentariosUsuarios[c.owner.username] = diccionarioComentariosUsuarios[c.owner.username] + 1
            if(diccionarioComentariosUsuarios.get(c.owner.username) > maxComentarios.comentarios):
                maxComentarios = UsuarioMaxComentariosClass(c.owner.username,diccionarioComentariosUsuarios[c.owner.username])
        else:
            diccionarioComentariosUsuarios[c.owner.username] = 1

            
        for a in c.answers:
            contador += 1
            if(comentarioMaxLikes.likes < a.likes_count):
                comentarioMaxLikes = ComentarioMaxLikesClass(a.owner.username, a.created_at_utc, a.likes_count, a.text)

            if( a.owner.username in diccionarioComentariosUsuarios):
                diccionarioComentariosUsuarios[a.owner.username] = diccionarioComentariosUsuarios[a.owner.username] + 1
                if(diccionarioComentariosUsuarios.get(a.owner.username) > maxComentarios.comentarios):
                    maxComentarios = UsuarioMaxComentariosClass(a.owner.username,diccionarioComentariosUsuarios[a.owner.username])
            else:
                diccionarioComentariosUsuarios[a.owner.username] = 1
            

    if ((tiempoTranscurrido > 30) or (contador == 0)):
        return '',''
    else:
        return comentarioMaxLikes, maxComentarios
        

##----------------------------------------------------------------------##
##-------------------------Highlights de perfil-------------------------##
##----------------------------------------------------------------------##

def informacionHightlightsCuenta(IdentificadorCuenta,cuentaScrapeo):
    try:
        context = {}

        contadorHighlights = 0
        contadorSalida = 0                                                #Contador para dejar de buscar historias de highlights

        listaHighlightIntermedia = []

        comienzo = monotonic()                                            #Temporizador para parar la ejecución si hay muchas historias

        cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)
        
        for highlights in cuentaBuscadora.get_highlights(IdentificadorCuenta):          #Recupera las historias destacadas para un usuario id ordenadas de más reciente a menos
            contadorHighlights += 1
            listaHistoriasDestacadas = []
            numeroImagenes = 0
            numeroVideos = 0

            fin = monotonic()
            tiempoTranscurrido = fin - comienzo
            #Temporizador de 30 segundos
            if(tiempoTranscurrido > 30):
                break

            url_post = INSTAGRAM + HIGHLIGHT + str(highlights.unique_id) + '/'

            for historia in highlights.get_items():
                contadorSalida += 1

                if(historia.typename == 'GraphStoryVideo'): 
                    tipo_publicacion ='Video'
                    numeroVideos += 1
                    #url_story = historia.video_url                 #A la hora de conseguir la URL de la imagen, da error
                    duracion = historia._node['video_duration']                  
                else: 
                    tipo_publicacion ='Imagen'
                    numeroImagenes += 1
                    #url_story = historia.url                       #A la hora de conseguir la URL de la imagen, da error
                    duracion = 5.0                  

                url_story ='No funciona'
                listaHistoriasDestacadas.append(StoryClass(tipo_publicacion, historia.date_local, duracion, url_story))

            listaHighlightIntermedia.append(HihglightClass(highlights.title, highlights.itemcount, highlights.cover_url, url_post, numeroImagenes, numeroVideos, listaHistoriasDestacadas))

        if (contadorHighlights == 0):                          #Si no tiene historias destacadas no devolvemos diccionario
            return None                          
        else:
            context['destacados'] = listaHighlightIntermedia
            context['contadorHighlights'] = contadorHighlights
            return context

    except Exception as e: 
        traceback.print_exc()
        return None


##---------------------------------------------------------------------##
##-------------------------Busqueda de hashtag-------------------------##
##---------------------------------------------------------------------##

def buscadorHashtag(queryset,cuentaScrapeo):
    contador = 0
    listaHashtags = []
    diccionarioHashtags = {}

    cuentaBuscadora = comprobarCuentaBuscadora(cuentaScrapeo)

    for hashtag in TopSearchResults(cuentaBuscadora.context,queryset).get_hashtag_strings():
        contador += 1
        listaHashtags.append(hashtag)

    diccionarioHashtags = {
    'contador': contador,
    'listaHashtags': listaHashtags
    }

    return diccionarioHashtags
from instaloader import Instaloader, Profile
import traceback

USER = 'instaanalysistfg'
PASS = 'juliogamer0423'
INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'
HIGHLIGHT = 'stories/highlights/'



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

class StoryClass:

    def __init__(self, tipo, fecha, duracion, url):
        self.tipo = tipo
        self.fecha = fecha
        self.duracion = duracion
        self.url = url

    def __repr__(self):
        return '{' + self.tipo +  ', ' + str(self.fecha) + ', ' + str(self.duracion) +  ', '+ self.url +'}'



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

    for post in publicaciones:
        
        contador +=1
        if (contador > 20): break             #Cantidad de publicaciones a mostrar como máximo

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): tipo_publicacion ='Imagen'
        elif(post.typename == 'GraphVideo'): tipo_publicacion ='Video'
        else: tipo_publicacion ='Sidecar'
        
        listaInfoPostRecientes.append(PostClass(cuenta, post.likes, post.comments, tipo_publicacion, post.date_local, url_post))
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

        mediaLikes += post.likes
        mediaComentarios += post.comments
        mediaVisualizaciones += post.video_view_count

        url_post = INSTAGRAM + POST + post.shortcode + '/'
        listaInfoVideos.append(PostClassVideo(cuenta, post.video_view_count, post.likes, post.comments, post.date_local, url_post))
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

        mediaLikes += post.likes
        mediaComentarios += post.comments

        url_post = INSTAGRAM + POST + post.shortcode + '/'

        if(post.typename == 'GraphImage'): tipo_publicacion ='Imagen'
        elif(post.typename == 'GraphVideo'): tipo_publicacion ='Video'
        else: tipo_publicacion ='Sidecar'

        listaInfoPublicacionesEtiquetadas.append(PostClass(cuenta, post.likes, post.comments, tipo_publicacion, post.date_local, url_post))
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


##----------------------------------------------------------------------##
##-------------------------Highlights de perfil-------------------------##
##----------------------------------------------------------------------##

def informacionHightlightsCuenta(IdentificadorCuenta):
    try:
        context = {}

        contadorHighlights = 0
        contadorSalida = 0                                                #Contador para dejar de buscar historias de highlights
        
        for highlights in L.get_highlights(IdentificadorCuenta):          #Recupera las historias destacadas para un usuario id ordenadas de más reciente a menos
            contadorHighlights += 1
            listaHistoriasDestacadas = []
            numeroImagenes = 0
            numeroVideos = 0

            url_post = INSTAGRAM + HIGHLIGHT + str(highlights.unique_id) + '/'

            datos = {
            "titulo": highlights.title,
            "numero_historias": highlights.itemcount,                  
            "foto_portada": highlights.cover_url,  
            "url": url_post,
            }
            context[contadorHighlights] = datos
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
                    duracion = 5                  

                url_story ='No funciona'
                listaHistoriasDestacadas.append(StoryClass(tipo_publicacion, historia.date_local, duracion, url_story))

            context[contadorHighlights]['numeroImagenes'] = numeroImagenes
            context[contadorHighlights]['numeroVideos'] = numeroVideos
            context[contadorHighlights]['listaHistoriasDestacadas'] = listaHistoriasDestacadas

            if(contadorSalida >= 200): break                   #Dejamos de buscar cuando llevemos 200 historias


        if (contadorHighlights == 0):                          #Si no tiene historias destacadas no devolvemos diccionario
            return None                          
        else: 
            context['contadorHighlights'] = contadorHighlights
            return context

    except Exception as e: 
        traceback.print_exc()
        return None
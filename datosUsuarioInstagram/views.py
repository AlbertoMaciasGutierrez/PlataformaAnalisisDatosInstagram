import os
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datosUsuarioInstagram.instaloader_funciones import informacionCuenta, informacionHightlightsCuenta, buscadorPerfil, buscadorHashtag, informacionPost, buscadorPost, iniciarSesion
from datosUsuarioInstagram.utils import HihglightClass, StoryClass
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from cuentas.models import Usuario
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalUpdateView, BSModalCreateView





@login_required
@require_http_methods(["GET"])
def renderizarHome(request):
    return render(request, os.path.join("home", "home.html"))

@login_required
@require_http_methods(["GET","POST"])
def renderizarContacto(request):
    context = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            context['mensaje'] = 'Petición guardada'
            messages.success(request, 'Peticion enviada correctamente')
            return redirect ('/analisisInsta/contacto')
        else:
            context['form'] = form
    
    return render(request, os.path.join("contacto", "contacto.html"),context=context)






##-------------------------------------------------------------##
##----------------------------USUARIOS-------------------------##
##-------------------------------------------------------------##

@login_required
@require_http_methods(["GET","POST","DELETE"])
def addCuentasBaseDatos(request,IDusuario):
    #Comprobamos si el usuario tiene cuentas para scrapear usando
    cuentaScrapeo = comprobarCuentaScrapeo(request)

    context = {}
    context = informacionCuenta(IDusuario, cuentaScrapeo)
    context['IDcuenta'] = IDusuario

    diccionario_datos = {}
    diccionario_datos.update(context)
    del diccionario_datos['ID_usuario']
    del diccionario_datos['listaInfoPostRecientes']
    del diccionario_datos['listaInfoVideos']
    del diccionario_datos['listaInfoPublicacionesEtiquetadas']

    form = BusquedaUsuarioForm(diccionario_datos)
    if form.is_valid():
        form.save()
        messages.success(request, 'Busqueda actualizada correctamente')

    
    #Añadimos los correspondientes post, videos y post etiquetados a la base de datos 
    for lista in context['listaInfoPostRecientes']:
        form = BusquedaUsuarioPostForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                        'tipo': lista.tipo, 'fecha': lista.fecha, 'url': lista.url, 'shortcode': lista.shortcode})
        if form.is_valid():
            form.save()

    for lista in context['listaInfoVideos']:
        form = BusquedaUsuarioVideosForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                                'reproducciones': lista.reproducciones, 'fecha': lista.fecha, 'url': lista.url, 'shortcode': lista.shortcode})
        if form.is_valid():
            form.save()

    for lista in context['listaInfoPublicacionesEtiquetadas']:
        form = BusquedaUsuarioEtiquetadasForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                                'tipo': lista.tipo, 'fecha': lista.fecha, 'url': lista.url, 'shortcode': lista.shortcode})
        if form.is_valid():
            form.save()

    #Añadimos el número de ID de usuario
    form = BusquedaUsuarioIDusuarioForm({'cuentaID': context['IDcuenta'], 'usuarioID': context['ID_usuario']})
    if form.is_valid():
        form.save()
    
    return context


@login_required
@require_http_methods(["GET"])
def actualizarCuentasBaseDatos(request,IDusuario):
    
    try:
        objetoUsuarioID = DatosBusquedaUsuario.objects.get(IDcuenta = IDusuario)

        diferencia_timer = timezone.now() - objetoUsuarioID.timer
        minutos = diferencia_timer.seconds/60
        #Si hay una diferencia de 3 minutos entre el tiempo de creación y el actual borramos y volvemos a añadir la búsqueda
        if(minutos >= 3):
            #Borramos y volvemos a realizar la busqueda, introducimos los datos en la base de datos y los devolvemos
            objetoUsuarioID.delete()
            context = addCuentasBaseDatos(request,IDusuario)
            
            return context

        else:
            #Recuperamos los datos de la base de datos y los retornamos en forma de diccionario
            objetoUsuarioID = objetoUsuarioID.__dict__                   #Convertimos el objeto a diccionario para pasarlo al template
            del objetoUsuarioID['_state']                                #Borramos esta clave innecesaria del diccionario

            objetoUsuarioID['listaInfoPostRecientes'] = DatosPostBusquedaUsuario.objects.filter(cuentaID = IDusuario)
            objetoUsuarioID['listaInfoVideos'] = DatosVideosBusquedaUsuario.objects.filter(cuentaID = IDusuario)
            objetoUsuarioID['listaInfoPublicacionesEtiquetadas'] = DatosEtiquetadasBusquedaUsuario.objects.filter(cuentaID = IDusuario)

            return objetoUsuarioID


    except:
        #Realizamos la búsqueda, introducimos los datos en la base de datos y los devolvemos
        context = addCuentasBaseDatos(request,IDusuario)
        
        return context




@login_required
@require_http_methods(["GET"])
def obtenerInformacionCuenta(request,IDusuario):

    info = actualizarCuentasBaseDatos(request,IDusuario)
    
    return render(request, os.path.join("cuentas_Instagram", "info_cuenta.html"),context=info)


@login_required
@require_http_methods(["GET"])
def bucadorCuentas(request):

    queryset = request.GET.get("Buscar")
    #Comprobamos si el usuario tiene cuentas para scrapear usando
    cuentaScrapeo = comprobarCuentaScrapeo(request)

    if queryset:
        info = buscadorPerfil(queryset,cuentaScrapeo)
        return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=info )

    elif (queryset == ''):
        buscado = True
        return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"),{'buscado':buscado, 'cuentaScrapeo': cuentaScrapeo})

    return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"), {'cuentaScrapeo': cuentaScrapeo})


##---------------------------------------------------------##
##----------------------------POST-------------------------##
##---------------------------------------------------------##

@login_required
@require_http_methods(["GET","POST","DELETE"])
def addPublicacionesBaseDatos(request,IdentificadorPost):
    #Comprobamos si el usuario tiene cuentas para scrapear usando
    cuentaScrapeo = comprobarCuentaScrapeo(request)

    context = {}
    context = informacionPost(IdentificadorPost,cuentaScrapeo)

    diccionario_datos = {}
    diccionario_datos.update(context)
    del diccionario_datos['listaPostSidecar']
    del diccionario_datos['listaHastagsSustitulo']
    del diccionario_datos['listaMecionesSustitulo']
    del diccionario_datos['listaPatrocinadoresPost']
    del diccionario_datos['listaUsuariosEtiquetados']
    del diccionario_datos['comentarioMaxPopular']
    del diccionario_datos['usuarioMaxComenta']

    form = BusquedaPostForm(diccionario_datos)
    if form.is_valid():
        form.save()
        messages.success(request, 'Busqueda actualizada correctamente')

    #Añadimos comentario com más likes y usuario que más comenta en el post
    if((context['comentarioMaxPopular'] != '') and (context['usuarioMaxComenta'] != '')):
        form = ComentarioMaxLikesPostForm({'shortcode': IdentificadorPost, 'propietario': context['comentarioMaxPopular'].propietario, 
                                            'fecha': context['comentarioMaxPopular'].fecha, 'likes': context['comentarioMaxPopular'].likes, 
                                            'text': context['comentarioMaxPopular'].text})
        if form.is_valid():
            form.save()

        form = UsuarioMaxComentariosPostForm({'shortcode': IdentificadorPost, 'nombre': context['usuarioMaxComenta'].nombre, 
                                            'comentarios': context['usuarioMaxComenta'].comentarios})
        if form.is_valid():
            form.save()

    #Añadimos post sidecar, hashtags y menciones en subtitulo, patrocinadores y usuarios etiquetados en el post
    for lista in context['listaPostSidecar']:
        form = PostSidecarForm({'shortcode': IdentificadorPost, 'numero':lista.numero , 'tipo': lista.tipo, 
                                'url': lista.url})
        if form.is_valid():
            form.save()

    for lista in context['listaHastagsSustitulo']:
        form = HashtagsSubtituloPostForm({'shortcode': IdentificadorPost, 'hashtag':lista})
        if form.is_valid():
            form.save()
    
    for lista in context['listaMecionesSustitulo']:
        form = MencionesSubtituloPostForm({'shortcode': IdentificadorPost, 'mencion':lista})
        if form.is_valid():
            form.save()
    
    for lista in context['listaPatrocinadoresPost']:
        form = PatrocinadoresPostForm({'shortcode': IdentificadorPost, 'patrocinador':lista})
        if form.is_valid():
            form.save()
    
    for lista in context['listaUsuariosEtiquetados']:
        form = UsuariosEtiquetadosPostForm({'shortcode': IdentificadorPost, 'usuario':lista})
        if form.is_valid():
            form.save()

    
    return context


@login_required
@require_http_methods(["GET"])
def actualizarPublicacionesBaseDatos(request,IdentificadorPost):
    
    try:
        objetodentificadorPost = DatosPost.objects.get(shortcode = IdentificadorPost)

        diferencia_timer = timezone.now() - objetodentificadorPost.timer
        minutos = diferencia_timer.seconds/60
        #Si hay una diferencia de 3 minutos entre el tiempo de creación y el actual borramos y volvemos a añadir la búsqueda
        if(minutos >= 3):
            #Borramos y volvemos a realizar la busqueda, introducimos los datos en la base de datos y los devolvemos
            objetodentificadorPost.delete()
            context = addPublicacionesBaseDatos(request,IdentificadorPost)
            
            return context

        else:
            #Recuperamos los datos de la base de datos y los retornamos en forma de diccionario
            objetodentificadorPost = objetodentificadorPost.__dict__                   #Convertimos el objeto a diccionario para pasarlo al template
            del objetodentificadorPost['_state']                                #Borramos esta clave innecesaria del diccionario

            if(objetodentificadorPost['tipo'] == 'Sidecar'):
                objetodentificadorPost['listaPostSidecar'] = PostSidecar.objects.filter(shortcode = IdentificadorPost)
            
            try:
                objeto= HashtagsSubtituloPost.objects.filter(shortcode = IdentificadorPost)
                lista = []
                for obj in objeto:
                    lista.append(obj.hashtag)
                objetodentificadorPost['listaHastagsSustitulo'] = lista
            except:
                objetodentificadorPost['listaHastagsSustitulo'] = []

            try:
                objeto= MencionesSubtituloPost.objects.filter(shortcode = IdentificadorPost)
                lista = []
                for obj in objeto:
                    lista.append(obj.mencion)
                objetodentificadorPost['listaMecionesSustitulo'] = lista
            except:
                objetodentificadorPost['listaMecionesSustitulo'] = []

            try:
                objeto= PatrocinadoresPost.objects.filter(shortcode = IdentificadorPost)
                lista = []
                for obj in objeto:
                    lista.append(obj.patrocinador)
                objetodentificadorPost['listaPatrocinadoresPost'] = lista
            except:
                objetodentificadorPost['listaPatrocinadoresPost'] = []

            try:
                objeto= UsuariosEtiquetadosPost.objects.filter(shortcode = IdentificadorPost)
                lista = []
                for obj in objeto:
                    lista.append(obj.usuario)
                objetodentificadorPost['listaUsuariosEtiquetados'] = lista
            except:
                objetodentificadorPost['listaUsuariosEtiquetados'] = []

            try:
                objetodentificadorPost['comentarioMaxPopular'] = ComentarioMaxLikesPost.objects.get(shortcode = IdentificadorPost)
            except:
                objetodentificadorPost['comentarioMaxPopular'] = ''

            try:
                objetodentificadorPost['usuarioMaxComenta'] = UsuarioMaxComentariosPost.objects.get(shortcode = IdentificadorPost)
            except:
                objetodentificadorPost['usuarioMaxComenta'] = ''


            return objetodentificadorPost


    except:
        #Realizamos la búsqueda, introducimos los datos en la base de datos y los devolvemos
        context = addPublicacionesBaseDatos(request,IdentificadorPost)
        
        return context


login_required
@require_http_methods(["GET"])
def obtenerInformacionPost(request,IdentificadorPost):

    info = actualizarPublicacionesBaseDatos(request,IdentificadorPost)

    return render(request, os.path.join("publicacion", "info_post.html"),context=info)


@login_required
@require_http_methods(["GET"])
def buscadorPublicacion(request):

    queryset = request.GET.get("Buscar") 
    #Comprobamos si el usuario tiene cuentas para scrapear usando
    cuentaScrapeo = comprobarCuentaScrapeo(request)

    if queryset:
        info = buscadorPost(queryset,cuentaScrapeo)
        if(info == None):
            return render(request, os.path.join("publicacion", "listaBusquedaPost.html"))
        else:
            return render(request, os.path.join("publicacion", "listaBusquedaPost.html"),context=info )

    elif (queryset == ''):
        buscado = True
        return render(request, os.path.join("publicacion", "buscador_post.html"),{'buscado':buscado, 'cuentaScrapeo': cuentaScrapeo})

    return render(request, os.path.join("publicacion", "buscador_post.html"),{'cuentaScrapeo': cuentaScrapeo})








##---------------------------------------------------------------##
##----------------------------HIGHLIGHTS-------------------------##
##---------------------------------------------------------------##
#'''

@login_required
@require_http_methods(["GET"])
def obtenerHighlightsCuenta(request,IDusuario):
    identificadorCuenta = get_object_or_404(IdentificadorUsuario, cuentaID = IDusuario) 
    highlights = actualizarHighlightsBaseDatos(request,IDusuario,identificadorCuenta.usuarioID)
    highlights['IDcuenta'] = IDusuario

    return render(request, os.path.join("cuentas_Instagram", "highlights_cuenta.html"), context = highlights)



@login_required
@require_http_methods(["GET","POST"])
def actualizarHighlightsBaseDatos(request,IDusuario,identificadorCuenta):
    #Si existen los highlights los devolvemos como diccionario y si no hacemos la búsqueda y lo añadimos
    try:
        contadorHighlights = ContadorHighlights.objects.get(cuentaID = IDusuario)
        highlights = {'contadorHighlights': contadorHighlights.contadorHighlights}

        objetosHighlights = DatosHighlight.objects.filter(cuentaID = IDusuario)
        
        listaHighlightsIntermedia = []

        for destacados in objetosHighlights:
            listaHistoriasDestacadas = []

            objetosStoriesHighlight = DatosStoryHighlight.objects.filter(highlight = destacados.identificador_highlight_usuario)

            for historia in objetosStoriesHighlight:
                listaHistoriasDestacadas.append((StoryClass(historia.tipo, historia.fecha, historia.duracion, historia.url)))

            listaHighlightsIntermedia.append(HihglightClass(destacados.titulo, destacados.numero_historias, destacados.foto_portada, destacados.url, destacados.numeroImagenes, destacados.numeroVideos, listaHistoriasDestacadas))
            
            
        highlights['destacados'] = listaHighlightsIntermedia
        messages.success(request, 'Highlights cargados correctamente')
        return highlights
#'''
    except:
        #Comprobamos si el usuario tiene cuentas para scrapear usando
        cuentaScrapeo = comprobarCuentaScrapeo(request)

        highlights = informacionHightlightsCuenta(identificadorCuenta,cuentaScrapeo)

        if highlights == None:
            dicionarioVacio = {}
            return dicionarioVacio
        else:
            form = ContadorHighlightsForm({'cuentaID': IDusuario, 'contadorHighlights': highlights['contadorHighlights']})
            if form.is_valid():
                form.save()
                print('Contador añadido')

            for lista in highlights['destacados']:
                idetificador_highlight = IDusuario + '-' + lista.titulo
                form = HighlightForm({'cuentaID': IDusuario, 'identificador_highlight_usuario': idetificador_highlight, 'titulo': lista.titulo, 'numero_historias': lista.numero_historias, 
                                        'foto_portada': lista.foto_portada, 'url': lista.url,'numeroImagenes': lista.numeroImagenes, 'numeroVideos': lista.numeroVideos})
                if form.is_valid():
                    form.save()
                    #messages.success(request, 'Highlight añadido correctamente')

                    for historia in lista.listaHistoriasDestacadas:
                        form = HighlightStoryForm({'highlight' : idetificador_highlight , 'tipo': historia.tipo, 'fecha': historia.fecha,          
                                                    'duracion': historia.duracion, 'url': historia.url})
                        if form.is_valid():
                            form.save()
                            #print('Historia añadida correctamente')


        messages.success(request, 'Highlights añadidos correctamente')
        return highlights

#'''

##---------------------------------------------------------------##
##----------------------------HASHTAGS---------------------------##
##---------------------------------------------------------------##

@login_required
@require_http_methods(["GET"])
def obtenerInformacionHashtag(request,Hashtag):

    return render(request, os.path.join("hashtag", "info_hashtag.html"))


@login_required
@require_http_methods(["GET"])
def bucadorHashtag(request):

    queryset = request.GET.get("Buscar")
    #Comprobamos si el usuario tiene cuentas para scrapear usando
    cuentaScrapeo = comprobarCuentaScrapeo(request)

    if queryset: 
        info = buscadorHashtag(queryset,cuentaScrapeo)
        return render(request, os.path.join("hashtag", "listaBusquedaHashtag.html"),context=info)

    elif (queryset == ''):
        buscado = True
        return render(request, os.path.join("hashtag", "buscador_hashtag.html"),{'buscado':buscado, 'cuentaScrapeo': cuentaScrapeo})

    return render(request, os.path.join("hashtag", "buscador_hashtag.html"), {'cuentaScrapeo': cuentaScrapeo})



##-----------------------------------------------------------------------##
##--------------------CUENTAS INSTAGRAM PARA SCRAPEAR--------------------##
##-----------------------------------------------------------------------##

def comprobarCuentaScrapeo(request):
    usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
    cuentaScrapeo = ''

    for c in CuentaScrapeoInstagram.objects.filter(usuario = usuarioActual):
        if(c.usando == True):
            cuentaScrapeo = c.cuenta
            break

    return cuentaScrapeo


@login_required
@require_http_methods(["GET","POST","DELETE"])
def cuentasScrapingInstagram(request):
    usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
    context = {
        "cuentas_scrapeo_disponibles": CuentaScrapeoInstagram.objects.filter(usuario = usuarioActual)
        }

    return render(request, os.path.join("cuentas_scrapeo_instagram", "cuentasScrapeo.html"),context = context)


class CuentaScrapingCrear(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cuentas_scrapeo_instagram/cuentaScrapeo_confirm_add.html'
    form_class = AddCuentaScrapingForm
    success_message = 'Cuenta añadida correctamente'
    success_url = reverse_lazy('cuentasScrapearInstagram')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            print('Estoy dentro')
            usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
            cuentaScraping = form.save(commit=False)

            #Iniciamos sesión de Instagram y la guardamos en el sistema
            if(iniciarSesion(cuentaScraping.cuenta, form['password'].data) == False):
                messages.success(request, 'La cuenta no se ha podido añadir')
                return redirect ('/analisisInsta/cuentasScraping/')

            cuentaScraping.usuario = usuarioActual
            cuentaScraping.usando = True

            #Comprobamos que la cuentaScraping para dicho usuario no sea repetida
            for c in CuentaScrapeoInstagram.objects.filter(usuario = usuarioActual):
                if cuentaScraping.cuenta == c.cuenta:
                    messages.success(request, 'Cuenta a añadir repetida')
                    return redirect ('/analisisInsta/cuentasScraping/')
            #Comprobamos que solo se esté usando una cuenta de las almacenadas
            for c in CuentaScrapeoInstagram.objects.filter(usuario = usuarioActual):
                if((c.usando == True) and (cuentaScraping.cuenta != c.cuenta)):
                    c.usando = False
                    c.save()

            return self.form_valid(form)
        else:
            print('Estoy fuera')
            return self.form_invalid(form)
            


class CuentaScrapingUsar(LoginRequiredMixin, BSModalUpdateView):
    model = CuentaScrapeoInstagram
    template_name = 'cuentas_scrapeo_instagram/cuentaScrapeo_confirm_use.html'
    form_class = UseCuentaScrapingForm
    success_message = 'Cuenta preparada para usar'
    success_url = reverse_lazy('cuentasScrapearInstagram')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        #Comprobamos que solo se esté usando una cuenta de las almacenadas
        #'''
        if(form['usando'].data):
            usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
            for c in CuentaScrapeoInstagram.objects.filter(usuario = usuarioActual):
                if((c.usando == True) and (self.object.cuenta != c.cuenta)):
                    c.usando = False
                    c.save()
        #'''
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class CuentaScrapingEliminar(LoginRequiredMixin, BSModalDeleteView):
    model = CuentaScrapeoInstagram
    template_name = 'cuentas_scrapeo_instagram/cuentaScrapeo_confirm_delete.html'
    success_message = 'Cuenta borrada correctamente'
    success_url = reverse_lazy('cuentasScrapearInstagram')



##--------------------------------------------------------------------##
##-------------------------MANEJO DE USUARIOS-------------------------##
##--------------------------------------------------------------------##

class RegistroUsuario(CreateView):
    model = Usuario
    template_name = 'registration/registrar.html'
    form_class = RegistroForm
    

    def form_valid(self, form):
        '''
        En este parte, si el formulario es valido guardamos lo que se obtiene de él y usamos authenticate para que el usuario incie sesión luego de haberse registrado y lo redirigimos al home
        '''
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('/analisisInsta')


class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def eliminarUsuario(request):
    if (request.POST):
        print("Eliminamos cuenta")
        usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
        usuarioActual.delete()
        return redirect ('/login')

    return render(request, os.path.join("registration", "delete.html"))


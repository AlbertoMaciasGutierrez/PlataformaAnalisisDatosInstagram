from multiprocessing import context
import os
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datosUsuarioInstagram.instagramy_funciones import modificarSesion_id, informacionHashtag
from datosUsuarioInstagram.instaloader_funciones import informacionCuenta, informacionHightlightsCuenta
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
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalUpdateView


datosHashtag = {}  #Diccionario global para pasar los datos del hashtag a los templates en obtenerInformacionHashtag         


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
@require_http_methods(["GET"])
def obtenerInformacionCuenta(request,IDusuario):
    objetoUsuarioID = get_object_or_404(DatosBusquedaUsuario, IDcuenta = IDusuario)
    objetoUsuarioID = objetoUsuarioID.__dict__                   #Convertimos el objeto a diccionario para pasarlo al template
    del objetoUsuarioID['_state']                                #Borramos esta clave innecesaria del diccionario

    objetoUsuarioID['listaInfoPostRecientes'] = DatosPostBusquedaUsuario.objects.filter(cuentaID = IDusuario)
    objetoUsuarioID['listaInfoVideos'] = DatosVideosBusquedaUsuario.objects.filter(cuentaID = IDusuario)
    objetoUsuarioID['listaInfoPublicacionesEtiquetadas'] = DatosEtiquetadasBusquedaUsuario.objects.filter(cuentaID = IDusuario)

    return render(request, os.path.join("cuentas_Instagram", "info_cuenta.html"),context=objetoUsuarioID)


@login_required
@require_http_methods(["GET"])
def bucadorCuentas(request):

    queryset = request.GET.get("Buscar")
    #print(queryset) 

    if queryset:
        context = {}
        context['IDcuenta'] = queryset
        info = informacionCuenta(queryset)

        if info == None:
            del context['IDcuenta']
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )
        else:
            #Para guardar los datos dentro de la base de datos y posteriormente usarlos
            context.update(info)
            rellenarFormularioCuentas(request,context)
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )

    elif (queryset == ''):
        buscado = True
        return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"),{'buscado':buscado})

    return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"))


@login_required
@require_http_methods(["GET","POST","DELETE"])
def rellenarFormularioCuentas(request,context):

    diccionario_datos = {}
    diccionario_datos.update(context)
    del diccionario_datos['ID_usuario']
    del diccionario_datos['listaInfoPostRecientes']
    del diccionario_datos['listaInfoVideos']
    del diccionario_datos['listaInfoPublicacionesEtiquetadas']

    #Si existe la busqueda la borramos y la volvemos a añadir y si no solamente la añadimos
    try:
        objetoUsuarioID = DatosBusquedaUsuario.objects.get(IDcuenta = context['IDcuenta'])
        objetoUsuarioID.delete()
        form = BusquedaUsuarioForm(diccionario_datos)
        if form.is_valid():
            form.save()
            messages.success(request, 'Busqueda actualizada correctamente') 

    except:
        form = BusquedaUsuarioForm(diccionario_datos)
        if form.is_valid():
            form.save()
            messages.success(request, 'Busqueda añadida correctamente')

    #Añadimos los correspondientes post, videos y post etiquetados a la base de datos 
    for lista in context['listaInfoPostRecientes']:
        form = BusquedaUsuarioPostForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                        'tipo': lista.tipo, 'fecha': lista.fecha, 'url': lista.url})
        if form.is_valid():
            form.save()

    for lista in context['listaInfoVideos']:
        form = BusquedaUsuarioVideosForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                                'reproducciones': lista.reproducciones, 'fecha': lista.fecha, 'url': lista.url})
        if form.is_valid():
            form.save()

    for lista in context['listaInfoPublicacionesEtiquetadas']:
        form = BusquedaUsuarioEtiquetadasForm({'cuentaID': context['IDcuenta'], 'likes': lista.likes, 'comentarios': lista.comentarios, 
                                                'tipo': lista.tipo, 'fecha': lista.fecha, 'url': lista.url})
        if form.is_valid():
            form.save()

    #Añadimos el número de ID de usuario
    form = BusquedaUsuarioIDusuarioForm({'cuentaID': context['IDcuenta'], 'usuarioID': context['ID_usuario']})
    if form.is_valid():
        form.save()




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
        highlights = informacionHightlightsCuenta(identificadorCuenta)

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

##-----------------------------------------------------------------------##
##----------------------------INSTAGRAMHASHTAG---------------------------##
##-----------------------------------------------------------------------##

@login_required
@require_http_methods(["GET"])
def obtenerInformacionHashtag(request,Hashtag):
    
    #Hacemos una lista con los likes para los gráficos
    likes = []
    for l in datosHashtag['listaInfoPosts']:
        likes.append(l.likes)
        
    datosHashtag['likes'] = likes

    return render(request, os.path.join("hashtag", "info_hashtag.html"),context=datosHashtag)


@login_required
@require_http_methods(["GET"])
def bucadorHashtag(request):

    queryset = request.GET.get("Buscar")
    #print(queryset) 

    if queryset: 
        context = informacionHashtag(queryset)

        if context == None:
            return render(request, os.path.join("hashtag", "listaBusquedaHashtag.html"),context=context )
        else:
            context['Hashtag'] = queryset
            datosHashtag.update(context)
            return render(request, os.path.join("hashtag", "listaBusquedaHashtag.html"),context=context )

    return render(request, os.path.join("hashtag", "buscador_hashtag.html"))



##--------------------------------------------------------------------##
##------------------------------IDSESION------------------------------##
##--------------------------------------------------------------------##

@login_required
@require_http_methods(["GET","POST","DELETE"])
def idSesion(request):
    usuarioActual = get_object_or_404(Usuario, pk = request.user.pk)
    sesionID = modificarSesion_id()
    

    if request.method == 'POST':
        form = IDSesionForm(request.POST)
        if form.is_valid():
            IDSesion = form.save(commit=False)
            IDSesion.usuario = usuarioActual
            
            #Comprobamos que el IDSesion para dicho usuario no sea repetido
            for ID in IDSesionUsuario.objects.filter(usuario = usuarioActual):
                if IDSesion.content == ID.content:
                    messages.success(request, 'IDSesion repetido')
                    return redirect ('/analisisInsta/IDSesion')

            IDSesion.save()
            messages.success(request, 'IDSesion añadido correctamente')
            return redirect ('/analisisInsta/IDSesion') 
    else:
        form = IDSesionForm()

        context = {
            "sesionID": sesionID,
            "form":form,
            "idSesion_disponibles": IDSesionUsuario.objects.filter(usuario = usuarioActual)
            }


    return render(request, os.path.join("id_sesion", "idSesion.html"),context = context)


class IDSeionEliminar(LoginRequiredMixin, BSModalDeleteView):
    model = IDSesionUsuario
    template_name = 'id_sesion/idSesion_confirm_delete.html'
    success_message = 'IDSesion borrado correctamente'
    success_url = reverse_lazy('IDSesion')

class IDSeionEditar(LoginRequiredMixin, BSModalUpdateView):
    model = IDSesionUsuario
    template_name = 'id_sesion/idSesion_confirm_update.html'
    form_class = IDSesionUpdateForm
    success_message = 'IDSesion editado correctamente'
    success_url = reverse_lazy('IDSesion')



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
        # messages.success(request, "Registro completado correctamente")
        return redirect('/analisisInsta')

    #Pasamos una nueva variable al Template base.html   #QUITAR ESTO PARA LA PRÓXIMA
    def get_context_data(self, **kwargs):
        context = super(RegistroUsuario, self).get_context_data(**kwargs)
        #context['boton_activado'] = False                                      #Si boton_activado es verdadero el botón del buscador funciona, si es falso no
        return context    



class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm



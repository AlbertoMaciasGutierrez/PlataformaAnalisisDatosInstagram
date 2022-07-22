from multiprocessing import context
import os
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datosUsuarioInstagram.instagramy_funciones import modificarSesion_id, informacionHashtag
from datosUsuarioInstagram.instaloader_funciones import informacionCuenta
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from cuentas.models import Usuario
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm, IDSesionForm, IDSesionUpdateForm, ContactoForm, BusquedaUsuarioForm, ActualizacionBusquedaUsuarioForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalUpdateView


datosUsuario = {}  #Diccionario global para pasar los datos del usuario a los templates en obtenerInformacionCuenta
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
    return render(request, os.path.join("cuentas_Instagram", "info_cuenta.html"),context=datosUsuario)


@login_required
@require_http_methods(["GET"])
def bucadorCuentas(request):

    queryset = request.GET.get("Buscar")
    #print(queryset) 

    if queryset:
        context = {}
        context['IDcuenta'] = queryset 
        context.update(informacionCuenta(queryset))

        if context == None:
            del context['IDcuenta']
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )
        else:
            datosUsuario.update(context)
            #Para guardar los datos dentro de la base de datos y posteriormente usarlos
            rellenarFormularioCuentas(request,context)
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )

    elif (queryset == ''):
        buscado = True
        return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"),{'buscado':buscado})

    return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"))


@login_required
@require_http_methods(["GET","POST","UPDATE"])
def rellenarFormularioCuentas(request,context):
    #Arreglar esto para introducir estos datos dentro de la base de datos
    diccionario_datos = {}
    diccionario_datos.update(context)
    del diccionario_datos['listaInfoPostRecientes']
    del diccionario_datos['listaInfoVideos']
    del diccionario_datos['listaInfoPublicacionesEtiquetadas']
    #---------------------------------------------------------------------#
    form = BusquedaUsuarioForm(diccionario_datos)
    print(diccionario_datos)
    
    #Añadimos nueva busqueda de usuarios a la base de datos y si ya está actualizamos todos sus datos excepto el IDusuario
    if form.is_valid():
        form.save()
        messages.success(request, 'Busqueda añadida correctamente')    
    else:                                                                                  
        objetoUsuarioID = get_object_or_404(DatosBusquedaUsuario, IDcuenta = context['IDcuenta'])
        #Arreglar esto para introducir estos datos dentro de la base de datos
        dicionario_datos_actualizacion = {}
        dicionario_datos_actualizacion.update(diccionario_datos)
        del dicionario_datos_actualizacion['IDcuenta']
        #---------------------------------------------------------------------#
        form = ActualizacionBusquedaUsuarioForm(dicionario_datos_actualizacion, instance = objetoUsuarioID)
        if form.is_valid():
            form.save()
            messages.success(request, 'Busqueda actualizada correctamente') 



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



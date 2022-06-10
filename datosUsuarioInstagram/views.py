import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datosUsuarioInstagram.instagramy_funciones import informacionCuenta
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from cuentas.models import Usuario
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm


datos = {}  #Variable global para pasar los datos del usuario a los templates en obtenerInformacionCuenta           

# Create your views here.

@login_required
def renderizarHome(request):
    return render(request, os.path.join("home", "home.html"),context=datos)


@login_required
def obtenerInformacionCuenta(request,IDusuario):
    
    return render(request, os.path.join("cuentas_Instagram", "info_cuenta.html"),context=datos)


@login_required
def bucadorCuentas(request):

    queryset = request.GET.get("Buscar")
    #print(queryset) 

    if queryset: 
        context = informacionCuenta(queryset)

        if context == None:
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )
        else:
            context['IDcuenta'] = queryset
            datos.update(context)
            return render(request, os.path.join("cuentas_Instagram", "listaBusquedaCuenta.html"),context=context )

    return render(request, os.path.join("cuentas_Instagram", "buscador_cuenta.html"))








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



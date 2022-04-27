import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datosUsuarioInstagram.instagramy_funciones import informacionCuenta
from django.contrib.auth import login, authenticate
from cuentas.models import Usuario
from django.views.generic import CreateView
from .forms import RegistroForm


# Create your views here.


def obtenerInformacionCuenta(request):
    info = informacionCuenta("macy_guty")
    print(info)
    return render(request, os.path.join("cuentas_Instagram", "info_cuenta.html"))

class RegistroUsuario(CreateView):
    model = Usuario
    template_name = 'registration/registrar.html'
    form_class = RegistroForm
    

    def form_valid(self, form):
        '''
        En este parte, si el formulario es valido guardamos lo que se obtiene de él y usamos authenticate para que el usuario incie sesión luego de haberse registrado y lo redirigimos al index
        '''
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
       # messages.success(request, "Registro completado correctamente")
        return redirect('obternerInformacionCuenta')

    #Pasamos una nueva variable al Template base.html
    def get_context_data(self, **kwargs):
        context = super(RegistroUsuario, self).get_context_data(**kwargs)
        context['boton_activado'] = False                                      #Si boton_activado es verdadero el botón del buscador funciona, si es falso no
        return context    
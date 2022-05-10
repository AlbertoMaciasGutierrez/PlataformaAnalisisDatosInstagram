"""plataformaAnalisisDatosInstagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from datosUsuarioInstagram import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analisisInsta/buscadorCuenta/', views.bucadorCuentas, name="buscadorCuentas"),
    #path('analisisInsta/buscadorCuenta/busqueda/<nombre>/', views.realizarBusqueda, name="realizarBusqueda"),
    path('analisisInsta/buscadorCuenta/busqueda/<IDusuario>/', views.obtenerInformacionCuenta, name="obtenerInformacionCuenta"),

    path('registro/',views.RegistroUsuario.as_view(), name='registro_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),                                      #Add Django site authentication urls (for login, logout, password management)
]

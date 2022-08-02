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
    path('analisisInsta/', views.renderizarHome, name="home"),
    path('analisisInsta/contacto', views.renderizarContacto, name="contacto"),

    #Cuentas Instagram
    path('analisisInsta/buscadorCuenta/', views.bucadorCuentas, name="buscadorCuentas"),
    path('analisisInsta/buscadorCuenta/busqueda/<IDusuario>/', views.obtenerInformacionCuenta, name="obtenerInformacionCuenta"),
    #Highlights
    path('analisisInsta/buscadorCuenta/busqueda/highlights/<IDusuario>/', views.obtenerHighlightsCuenta, name="obtenerHighlightsCuenta"),

    #Hashtag Instagram
    path('analisisInsta/buscadorHashtag/', views.bucadorHashtag, name="buscadorHashtag"),
    path('analisisInsta/buscadorHashtag/busqueda/<Hashtag>/', views.obtenerInformacionHashtag, name="obtenerInformacionHashtag"),

    #Post Instagram
    path('analisisInsta/buscadorPost/busqueda/<IdentificadorPost>/', views.obtenerInformacionPost, name="obtenerInformacionPublicacion"),


    path('analisisInsta/IDSesion/', views.idSesion, name="IDSesion"),
    path('analisisInsta/IDSesion//eliminar/<int:pk>', views.IDSeionEliminar.as_view(), name='idSesion_eliminar'), 
    path('analisisInsta/IDSesion//editar/<int:pk>', views.IDSeionEditar.as_view(), name='idSesion_editar'), 

    path('registro/',views.RegistroUsuario.as_view(), name='registro_usuario'),
    path('login/',views.LoginUsuario.as_view(), name='login_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),                                      #Add Django site authentication urls (for login, logout, password management)
]

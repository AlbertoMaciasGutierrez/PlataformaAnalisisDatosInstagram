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
from django.conf.urls import handler404, handler500, handler403, handler400

handler404 = 'datosUsuarioInstagram.views.error_404'
handler500 = 'datosUsuarioInstagram.views.error_500'
handler403 = 'datosUsuarioInstagram.views.error_403'
handler400 = 'datosUsuarioInstagram.views.error_400'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('analisisInsta/', views.renderizarHome, name="home"),
    path('analisisInsta/contacto', views.renderizarContacto, name="contacto"),

    #Cuentas Instagram
    path('analisisInsta/buscadorCuenta/', views.bucadorCuentas, name="buscadorCuentas"),
    path('analisisInsta/buscadorCuenta/busqueda/<IDusuario>/', views.obtenerInformacionCuenta, name="obtenerInformacionCuenta"),
    #Highlights
    path('analisisInsta/buscadorCuenta/busqueda/highlights/<IDusuario>/', views.obtenerHighlightsCuenta, name="obtenerHighlightsCuenta"),

    #Post Instagram
    path('analisisInsta/buscadorPost/', views.buscadorPublicacion, name="buscadorPost"),
    path('analisisInsta/buscadorPost/busqueda/<IdentificadorPost>/', views.obtenerInformacionPost, name="obtenerInformacionPublicacion"),

    #Introducir cuentas de Instagram para Scrapear
    path('analisisInsta/cuentasScraping/', views.cuentasScrapingInstagram, name="cuentasScrapearInstagram"),
    path('analisisInsta/cuentasScraping/crear/', views.CuentaScrapingCrear.as_view(), name="cuentasScrapearInstagram_crear"),
    path('analisisInsta/cuentasScraping/usar/<int:pk>', views.CuentaScrapingUsar.as_view(), name="cuentasScrapearInstagram_usar"),
    path('analisisInsta/cuentasScraping/eliminar/<int:pk>', views.CuentaScrapingEliminar.as_view(), name="cuentasScrapearInstagram_eliminar"),

    #Manejo de usuarios
    path('registro/',views.RegistroUsuario.as_view(), name='registro_usuario'),
    path('login/',views.LoginUsuario.as_view(), name='login_usuario'),
    path('eliminarUsuario',views.eliminarUsuario, name='eliminar_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),                                      #Add Django site authentication urls (for login, logout, password management)
]

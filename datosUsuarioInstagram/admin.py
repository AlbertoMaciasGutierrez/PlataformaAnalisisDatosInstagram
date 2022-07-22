from django.contrib import admin
from .models import IDSesionUsuario, Contacto, DatosBusquedaUsuario

# Register your models here.
admin.site.register(IDSesionUsuario)
admin.site.register(Contacto)
admin.site.register(DatosBusquedaUsuario)
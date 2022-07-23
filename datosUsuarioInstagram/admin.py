from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(IDSesionUsuario)
admin.site.register(Contacto)
admin.site.register(DatosBusquedaUsuario)
admin.site.register(DatosPostBusquedaUsuario)
admin.site.register(DatosVideosBusquedaUsuario)
admin.site.register(DatosEtiquetadasBusquedaUsuario)

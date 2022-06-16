from os import device_encoding
from sqlite3 import Timestamp
from tabnanny import verbose
from django.db import models
from cuentas.models import Usuario
from django.utils import timezone


class IDSesionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    content = models.TextField()
    add_fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'IDSesionUsuario'
        verbose_name_plural = 'IDSesionUsuarios'
        ordering = ['-add_fecha']

    def __str__(self):
        return f'El IDSesion de {self.usuario} es {self.content}' 

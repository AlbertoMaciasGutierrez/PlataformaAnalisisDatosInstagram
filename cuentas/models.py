from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# Create your models here.

class Usuario(AbstractUser):                #Esto se hace por si se necesitan añadir más campos a la clase Usuario. Se debe hacer al principio porque sino más adelante no se puede
    
    first_name = models.CharField(_("nombre"), max_length=50, blank=False)
    last_name = models.TextField(_("apellidos"), max_length=100, blank=False)
    email = models.EmailField(_("correo"), blank=False)

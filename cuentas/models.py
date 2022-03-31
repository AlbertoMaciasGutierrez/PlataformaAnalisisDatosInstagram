from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):                #Esto se hace por si se necesitan añadir más campos a la clase Usuario
    pass                                    #Se debe hacer al principio porque sino más adelante no se puede
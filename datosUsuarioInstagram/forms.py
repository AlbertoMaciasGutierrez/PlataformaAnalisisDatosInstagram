from django import forms
from cuentas.models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _





class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=140, required=True)
    apellido = forms.CharField(max_length=140, required=False)
    correo = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username','correo','nombre','apellido','password1','password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Nombre de Usuario'})
        self.fields['correo'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Correo'})
        self.fields['nombre'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Nombre'})
        self.fields['apellido'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Apellido'})
        self.fields['password1'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Contraseña'})



class LoginForm(AuthenticationForm):
    error_messages = {
    "invalid_login":"",
    "inactive": _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Nombre de Usuario'})
        self.fields['password'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Contraseña'})




import email
from logging import PlaceHolder
from pdb import post_mortem
from django import forms
from cuentas.models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import IDSesionUsuario






class RegistroForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Nombre de Usuario'})
        self.fields['email'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Correo'})
        self.fields['first_name'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Nombre'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Apellidos',
                                                    'rows':'2'})
        self.fields['password1'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Contraseña'})


    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','password1','password2')

    


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


class IDSesionForm(forms.ModelForm):
    content = forms.CharField(label ='', widget= forms.Textarea(attrs={'class':'mt-2 mr-sm-3',
                                                                        'rows':1,
                                                                        'placeholder': "idSesion",
                                                                        'style':'max-width: 20rem; min-width: 20rem;'}), required=True)
    class Meta:
        model = IDSesionUsuario
        fields = ('content',)





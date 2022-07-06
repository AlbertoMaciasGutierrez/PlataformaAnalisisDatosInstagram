import email
from logging import PlaceHolder
from pdb import post_mortem
from django import forms
from cuentas.models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import IDSesionUsuario, Contacto
from bootstrap_modal_forms.forms import BSModalModelForm





class RegistroForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','password1','password2')


    username = forms.CharField(label ='Nombre de Usuario', widget= forms.TextInput(attrs={'class':'form-control mb-3',
                                                                    'placeholder':'Nombre de Usuario'}), required=True)

    first_name = forms.CharField(label ='Nombre', widget= forms.TextInput(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Nombre'}), required=True)

    last_name = forms.CharField(label ='Apellidos', widget= forms.Textarea(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Apellidos',
                                                                        'rows':'2'}), required=True)

    email = forms.CharField(label ='Correo', widget= forms.EmailInput(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Correo'}), required=True)

    password1 = forms.CharField(label ='Contraseña', strip =False, widget= forms.PasswordInput(attrs={'class':'form-control ',
                                                                        'placeholder':'Contraseña',
                                                                        "autocomplete": "new-password"}), required=True)

    password2 = forms.CharField(label ='Contraseña (Confirmación)', strip =False, widget= forms.PasswordInput(attrs={'class':'form-control ',
                                                                        'placeholder':'Contraseña (Confirmación)',
                                                                        "autocomplete": "new-password"}), required=True)

class LoginForm(AuthenticationForm):


    username = forms.CharField(label ='Nombre de Usuario', widget= forms.TextInput(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Nombre de Usuario',
                                                                        "autofocus": True}), required=True)

    password = forms.CharField(label ='Contraseña', strip =False, widget= forms.PasswordInput(attrs={'class':'form-control ',
                                                                        'placeholder':'Contraseña',
                                                                        "autocomplete": "current-password"}), required=True)


class IDSesionForm(forms.ModelForm):
    content = forms.CharField(label ='', widget= forms.Textarea(attrs={'class':'mt-2 mr-sm-3',
                                                                        'rows':1,
                                                                        'placeholder': "idSesion",
                                                                        'style':'max-width: 20rem; min-width: 20rem;'}), required=True)
    class Meta:
        model = IDSesionUsuario
        fields = ('content',)

class IDSesionUpdateForm(BSModalModelForm):
    content = forms.CharField(label ='', widget= forms.Textarea(attrs={'class':'mt-2 mr-sm-3',
                                                                        'rows':1,
                                                                        'placeholder': "idSesion",
                                                                        'style':'max-width: 20rem; min-width: 20rem;'}), required=True)

    class Meta:
        model = IDSesionUsuario
        fields = ('content',)


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ('nombre','correo','mensaje')
    
    nombre = forms.CharField(label ='', widget= forms.TextInput(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Nombre'}), required=True)
    
    correo = forms.CharField(label ='', widget= forms.TextInput(attrs={'class':'form-control mb-3',
                                                                        'placeholder':'Correo'}), required=True)
    
    mensaje = forms.CharField(label ='', widget= forms.Textarea(attrs={'class':'form-control',
                                                                        'rows':6,
                                                                        'placeholder': "Mensaje",}), required=True)
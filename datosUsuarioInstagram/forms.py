from django import forms
from cuentas.models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','password1','password2',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] ='form-control'
        self.fields['username'].widget.attrs['placeholder'] ='Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] ='form-control'
        self.fields['password'].widget.attrs['placeholder'] ='Contraseña'
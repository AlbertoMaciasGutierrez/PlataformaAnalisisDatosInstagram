from django import forms
from cuentas.models import Usuario
from django.contrib.auth.forms import UserCreationForm



class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','password1','password2',)
from django import forms
from django.core.validators import validate_email
from account.models import User

class RegisterForm(forms.Form):
    email = forms.EmailField( validators=[validate_email])

    class Meta:
        model = User
        fields = ['email','name','password','password2']
        widgets ={
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Brukernavn'
                    }
                ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Passord'
                }
            ),
        }
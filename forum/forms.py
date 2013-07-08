from django.contrib.auth.forms import AuthenticationForm
from django import forms
from models import Discussion, Comment

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = u'Brukernavn'
        self.fields['password'].widget.attrs['placeholder'] = u'Passord'

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'body')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': u'Tittel'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'data-widearea': 'enable'
                }
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'data-widearea': 'enable'
                }
            ),
        }
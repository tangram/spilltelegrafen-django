from django.contrib.auth.forms import AuthenticationForm
from django import forms
from models import Discussion, Comment

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = u'Brukernavn'
        self.fields['password'].widget.attrs['placeholder'] = u'Passord'

class DiscussionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(DiscussionForm, self).__init__(*args, **kwargs)
	    self.fields['title'].widget.attrs['placeholder'] = u'Tittel'

	class Meta:
		model = Discussion
		fields = ('title', 'body')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
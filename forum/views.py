from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from forms import LoginForm
from django.contrib import messages
from models import ForumTopic

def index(request):
    variables = {
        'pagetitle': 'Alle diskusjoner',
    }

    if not request.user.is_authenticated():
        variables['login_form'] = LoginForm()

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.error(request, u'Bruker er ikke aktiv')
        else:
            messages.error(request, u'Ugyldig brukernavn eller passord')

    return render(request, 'base_forum_index.html', variables)

def topic(request, slug=None):
    if slug:
        topic = get_object_or_404(ForumTopic, slug=slug)

    variables = {
        'topic': topic,
    }
    
    return render(request, 'topic_header.html', variables)
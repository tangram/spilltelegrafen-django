from django.shortcuts import render
from forms import LoginForm

def index(request):
    variables = {
        'page': {
            'title': 'Alle diskusjoner'
        },
    }

    if not request.user.is_authenticated():
        variables['login_form'] = LoginForm()

    return render(request, 'base_forum.html', variables)

def topic_header(request):
    variables = {}
    return render(request, 'topic_header.html', variables)

def topic(request):
    variables = {}
    return render(request, 'topic_header.html', variables)
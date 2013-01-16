from django.shortcuts import render, render_to_response

def index(request):
    return render_to_response('base_forum.html')

def topic_header(request):
    variables = {}
    return render('topic_header.html', variables)

def topic(request):
    variables = {}
    return render('topic_header.html', variables)
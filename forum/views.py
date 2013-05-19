from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from forms import LoginForm, DiscussionForm, CommentForm
from django.contrib import messages
from models import Discussion, Comment

def index(request):
    if not request.user.is_authenticated():
        discussions = None
        form = LoginForm()
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

    else:
        discussions = Discussion.objects.all()
        form = None

    variables = {
        'pagetitle': 'Alle diskusjoner',
        'discussions': discussions,
        'login_form': form,
    }

    return render(request, 'discussion_index.html', variables)

def get_discussion(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    variables = {
        'pagetitle': discussion.title,
        'discussion': get_object_or_404(Discussion, id=discussion_id),
        'form': CommentForm(),
    }

    return render(request, 'discussion.html', variables)

def post_discussion(request):
    if request.POST:
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save()
            discussion.author = request.user
            discussion.save()
            return redirect(discussion)
    else:
        form = DiscussionForm()

    variables = {
        'pagetitle': 'Ny diskusjon',
        'form': form,
    }

    return render(request, 'discussion_form.html', variables)

def ajax_get_comment(request, comment_id=None):
    variables = {
        'comment': get_object_or_404(Comment, id=comment_id),
    }
    return render(request, 'comment.html', variables) 

def ajax_post_comment(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.save()
            discussion.comments.add(comment)
            discussion.comment_count += 1
            discussion.last_commenter = request.user
            discussion.save()
            return render(request, 'comment.html', { 'comment': comment })

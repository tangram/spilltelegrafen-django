from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from forms import LoginForm, DiscussionForm, CommentForm
from models import Discussion, Comment
from core.models import User
from core.forms import UserForm
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    if not request.user.is_authenticated():
        form = LoginForm()
        discussions = None
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

    if request.user.is_authenticated():
        form = None
        discussions = Discussion.objects.order_by('-last_commented')

        try:
            page = request.GET.get('side', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(discussions, per_page=25, orphans=3, request=request)

        try:
            discussions = p.page(page)
        except EmptyPage:
            discussions = p.page(1)

    variables = {
        'pagetitle': 'Alle diskusjoner',
        'discussions': discussions,
        'login_form': form,
    }

    return render(request, 'discussion_index.html', variables)

def user_logout(request):
    logout(request)
    return redirect(index)

@login_required()
def get_own_discussions(request):
    discussions = Discussion.objects.filter(author=request.user).order_by('-last_commented')

    try:
        page = request.GET.get('side', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(discussions, per_page=25, orphans=3, request=request)

    try:
        discussions = p.page(page)
    except EmptyPage:
        discussions = p.page(1)

    variables = {
        'pagetitle': 'Alle diskusjoner',
        'discussions': discussions,
    }

    return render(request, 'discussion_index.html', variables)

@login_required()
def get_own_drafts(request):
    discussions = Discussion.objects.filter(author=request.user).filter(published=False).order_by('-created_time')

    try:
        page = request.GET.get('side', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(discussions, per_page=25, orphans=3, request=request)

    try:
        discussions = p.page(page)
    except EmptyPage:
        discussions = p.page(1)

    variables = {
        'pagetitle': 'Alle diskusjoner',
        'discussions': discussions,
    }

    return render(request, 'discussion_index.html', variables)

@login_required()
def get_discussion(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    from itertools import chain
    comments = list(chain([discussion], discussion.comments.all()))

    try:
        page = request.GET.get('side', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(comments, per_page=10, orphans=3, request=request)

    try:
        comments = p.page(page)
    except EmptyPage:
        comments = p.page(1)

    variables = {
        'pagetitle': discussion.title,
        'discussion': get_object_or_404(Discussion, id=discussion_id),
        'comments': comments,
        'form': CommentForm(),
    }

    return render(request, 'discussion.html', variables)

@login_required()
def post_discussion(request):
    if request.POST:
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save()
            discussion.author = request.user
            discussion.save()

            user = request.user
            user.discussion_count += 1
            user.save()

            return redirect(discussion)
    else:
        form = DiscussionForm()

    variables = {
        'pagetitle': 'Ny diskusjon',
        'form': form,
    }

    return render(request, 'discussion_form.html', variables)

@login_required()
def update_discussion(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if request.POST:
        if request.user == discussion.author or request.user.is_staff() or request.user.is_superuser:
            form = DiscussionForm(request.POST, instance=discussion)
            if form.is_valid():
                discussion = form.save()
                discussion.author = request.user
                discussion.save()

                return redirect(discussion)

@login_required()
def delete_discussion(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if request.POST:
        if request.user == discussion.author or request.user.is_staff() or request.user.is_superuser:
            user = discussion.author
            user.discussion_count -= 1
            user.save()

            discussion.delete()

    return redirect(index)

@login_required()
def ajax_get_comment(request, comment_id=None):
    variables = {
        'comment': get_object_or_404(Comment, id=comment_id),
    }
    return render(request, 'comment.html', variables)

@login_required()
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
            discussion.last_comment = comment
            discussion.save()

            user = request.user
            user.comment_count += 1
            user.save()

            return render(request, 'comment.html', { 'comment': comment })

@login_required()
def ajax_update_comment(request, discussion_id=None, comment_id=None):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.POST:
        if request.user == comment.author or request.user.is_staff() or request.user.is_superuser:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save()
                comment.save()

                return render(request, 'comment.html', { 'comment': comment })

@login_required()
def ajax_delete_comment(request, discussion_id=None, comment_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.POST:
        if request.user == comment.author or request.user.is_staff() or request.user.is_superuser:
            user = comment.author
            user.comment_count -= 1
            user.save()

            discussion.comment_count -= 1
            discussion.last_comment = discussion.comments.all()[:-1]
            discussion.last_commenter = discussion.last_comment.author
            discussion.save()

            comment.delete()

            if request.is_ajax():
                return HttpResponse('{ "status": "ok" }', content_type="application/json")

    return redirect(discussion.last_comment)

@login_required()
def ajax_kudos(request, discussion_id=None, comment_id=None):
    if discussion_id:
        discussion = get_object_or_404(Discussion, id=discussion_id)
        discussion.kudos.add(request.user)
        discussion.save()

    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.kudos.add(request.user)
        comment.save()

    if request.is_ajax():
        return HttpResponse('{ "status": "ok" }', content_type="application/json")

    return redirect(discussion.last_comment)

@login_required()
def ajax_unkudos(request, discussion_id=None, comment_id=None):
    if discussion_id:
        discussion = get_object_or_404(Discussion, id=discussion_id)
        discussion.kudos.remove(request.user)
        discussion.save()

    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.kudos.remove(request.user)
        comment.save()

    if request.is_ajax():
        return HttpResponse('{ "status": "ok" }', content_type="application/json")

    return redirect(discussion.last_comment)

@login_required()
def get_user(request, user_id=None):
    user = get_object_or_404(User, id=user_id)

    variables = {
        'pagetitle': user,
    }

    return render(request, 'user.html', variables)

@login_required()
def update_user(request, user_id=None):
    user = get_object_or_404(User, id=user_id)

    if request.POST:
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect(user)
    else:
        form = UserForm(instance=user)

    variables = {
        'pagetitle': 'Rediger profil',
        'form': form,
    }

    return render(request, 'user_form.html', variables)

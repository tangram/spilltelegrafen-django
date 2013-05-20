from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from forms import LoginForm, DiscussionForm, CommentForm
from models import Discussion, Comment
from core.models import Profile
from core.forms import ProfileForm

from pure_pagination import Paginator, PageNotAnInteger

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

    else:
        form = None
        discussions = Discussion.objects.order_by('-last_commented')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(discussions, per_page=25, orphans=3, request=request)
        discussions = p.page(page)

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
def get_discussion(request, discussion_id=None):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    from itertools import chain
    comments = list(chain([discussion], discussion.comments.all()))

    p = Paginator(comments, per_page=10, orphans=5, request=request)
    comments = p.page(page)

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

            profile = request.user.profile
            profile.discussion_count += 1
            profile.save()

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
            profile = discussion.author.profile
            profile.discussion_count -= 1
            profile.save()

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

            profile = request.user.profile
            profile.comment_count += 1
            profile.save()

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
            profile = comment.author.profile
            profile.comment_count -= 1
            profile.save()

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
def get_profile(request, profile_id=None):
    profile = get_object_or_404(Profile, id=profile_id)

    variables = {
        'pagetitle': profile.user,
    }

    return render(request, 'profile.html', variables)

@login_required()
def update_profile(request, profile_id=None):
    profile = get_object_or_404(Profile, id=profile_id)

    if request.POST:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.save()
            return redirect(profile)
    else:
        form = ProfileForm(instance=profile)

    variables = {
        'pagetitle': 'Rediger profil',
        'form': form,
    }

    return render(request, 'profile_form.html', variables)
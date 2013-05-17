# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# USERS
class UserProfile(models.Model):
    '''User profile, connected to a User'''
    user = models.OneToOneField(User)
    image = models.ImageField(
        u'Brukerbilde', upload_to='brukerbilder')

    mail_on_comment = models.BooleanField(
        u'Få mail ved svar på kommentar eller innlegg?', default=True)

    class Meta:
        app_label = u'auth'
        verbose_name = u'brukerprofil'
        verbose_name_plural = u'brukerprofiler'


# CONTENT
class Content(models.Model):
    '''Abstract base class for content (e.g. page, post)'''
    title = models.CharField(u'Tittel', max_length=255)
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(auto_now=True, editable=False)
    publish_time = models.DateTimeField(
        u'Publikasjonstidspunkt', auto_now_add=True)

    status = models.PositiveSmallIntegerField(default=1, editable=False)  # seems like a good idea
    comments = models.PositiveSmallIntegerField(default=0, editable=False)
    views = models.PositiveSmallIntegerField(default=0, editable=False)

    body = models.TextField(u'Brødtekst')

    published = models.BooleanField(u'Publisert', default=False)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        abstract = True


class Comment(models.Model):
    '''Abstract base class for comments.'''
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)

    created_time = models.DateTimeField(
        auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(
        auto_now=True, editable=False)

    body = models.TextField(u'Kommentar')

    def __unicode__(self):
        return u'%s...' % (self.body[0:50])

    class Meta:
        abstract = True


class Tag(models.Model):
    '''Generic tag model'''
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = u'tag'


class StaticPage(Content):
    '''Generic static page model'''
    class Meta:
        verbose_name = u'fast side'
        verbose_name_plural = u'faste sider'


# MEDIA
class Image(models.Model):
    '''Generic class for resizable images'''
    orig_image = models.ImageField(u'Originalt bilde', upload_to='originaler')

    # there must be some low level file stuff to be handled in an Image class

    class Meta:
        verbose_name = u'bilde'
        verbose_name_plural = u'bilder'


# FLAGS
class Flag(models.Model):
    '''Generic active boolean marking'''
    name = models.CharField(max_length=255)

    is_global = models.BooleanField(default=False)

    flag_text = models.CharField(max_length=255)
    flag_description = models.CharField(max_length=255)
    flagged_message = models.CharField(max_length=255)
    unflag_text = models.CharField(max_length=255)
    unflag_description = models.CharField(max_length=255)
    unflagged_message = models.CharField(max_length=255)

    SUBJECT_CHOICES = (
        (u'none',  u'Ingen'),
        (u'self',  u'Kun eget innhold'),
        (u'other', u'Kun andres innhold'),
    )
    subject_restriction = models.CharField(max_length=16, choices=SUBJECT_CHOICES)

    class Meta:
        abstract = True
        verbose_name = u'flagg'
        verbose_name_plural = u'flagg'
